from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import User, Speciality, Doctor, Appointment, Review, Notification
from .forms import (
    CustomUserCreationForm, CustomLoginForm, UserProfileForm, 
    DoctorProfileForm, AppointmentForm, ReviewForm, 
    DoctorSearchForm, AppointmentUpdateForm
)
from .decorators import admin_required, doctor_required, client_required

# --- Public Views ---

def index(request):
    """Home page showing top doctors and specialities"""
    specialities = Speciality.objects.all()[:6]
    top_doctors = Doctor.objects.filter(is_available=True).order_by('-rating')[:4]
    return render(request, 'medica911/index.html', {
        'specialities': specialities,
        'top_doctors': top_doctors
    })

def signup_view(request):
    """Unified signup for doctors and clients"""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    # Store role in session if it comes from a link (e.g., ?role=doctor)
    role_param = request.GET.get('role')
    if role_param in ['doctor', 'client']:
        request.session['selected_role'] = role_param
        request.session.modified = True  # Ensure it's saved before redirecting to Google


        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            user.role = role
            user.save()
            
            if role == 'doctor':
                # Create empty doctor profile
                Doctor.objects.create(user=user, license_number=f"PENDING-{user.id}")
                messages.success(request, "Account created! Please complete your medical profile.")
            else:
                messages.success(request, "Account created successfully!")
                
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'medica911/auth/signup.html', {'form': form})

def login_view(request):
    """Custom login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'medica911/auth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

# --- Shared Views ---

@login_required
def dashboard(request):
    """Redirect users to their respective dashboards based on role"""
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'doctor':
        return redirect('doctor_dashboard')
    else:
        return redirect('client_dashboard')

@login_required
def profile_edit(request):
    """Shared profile edit view"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'medica911/profile_edit.html', {'form': form})

# --- Admin Views ---

@admin_required
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    total_doctors = User.objects.filter(role='doctor').count()
    total_clients = User.objects.filter(role='client').count()
    total_appointments = Appointment.objects.count()
    
    # Simple trend: appointments in the last 7 days
    last_week = timezone.now() - timedelta(days=7)
    recent_appointments = Appointment.objects.filter(created_at__gte=last_week).count()
    
    pending_appointments = Appointment.objects.filter(status='pending').count()
    
    context = {
        'total_doctors': total_doctors,
        'total_clients': total_clients,
        'total_appointments': total_appointments,
        'recent_appointments': recent_appointments,
        'pending_appointments': pending_appointments,
        'latest_appointments': Appointment.objects.all().order_by('-created_at')[:5]
    }
    return render(request, 'medica911/admin/dashboard.html', context)

@admin_required
def manage_users(request, role):
    """View to manage doctors or clients"""
    users = User.objects.filter(role=role)
    return render(request, 'medica911/admin/manage_users.html', {
        'users': users,
        'role': role.capitalize()
    })

# --- Doctor Views ---

@doctor_required
def doctor_dashboard(request):
    """Doctor-specific dashboard"""
    doctor = request.user.doctor_profile
    upcoming = Appointment.objects.filter(
        doctor=doctor, 
        appointment_date__gte=timezone.now().date(),
        status__in=['pending', 'confirmed']
    ).order_by('appointment_date', 'appointment_time')
    
    return render(request, 'medica911/doctor/dashboard.html', {
        'doctor': doctor,
        'upcoming_appointments': upcoming
    })

@doctor_required
def doctor_profile_edit(request):
    """Doctor medical profile edit"""
    doctor = request.user.doctor_profile
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, "Medical profile updated!")
            return redirect('dashboard')
    else:
        form = DoctorProfileForm(instance=doctor)
    return render(request, 'medica911/doctor/profile_edit.html', {'form': form})

@doctor_required
def update_appointment(request, pk):
    """Doctor updates appointment status/notes"""
    appointment = get_object_or_404(Appointment, pk=pk, doctor=request.user.doctor_profile)
    if request.method == 'POST':
        form = AppointmentUpdateForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated!")
            return redirect('doctor_dashboard')
    else:
        form = AppointmentUpdateForm(instance=appointment)
    return render(request, 'medica911/doctor/update_appointment.html', {
        'form': form,
        'appointment': appointment
    })

# --- Client Views ---

@client_required
def client_dashboard(request):
    """Client-specific dashboard"""
    appointments = Appointment.objects.filter(client=request.user).order_by('-appointment_date')
    return render(request, 'medica911/client/dashboard.html', {
        'appointments': appointments
    })

def browse_doctors(request):
    """Search and filter doctors"""
    form = DoctorSearchForm(request.GET)
    doctors = Doctor.objects.filter(is_available=True)
    
    if form.is_valid():
        if form.cleaned_data.get('speciality'):
            doctors = doctors.filter(speciality=form.cleaned_data['speciality'])
        if form.cleaned_data.get('city'):
            doctors = doctors.filter(user__city__icontains=form.cleaned_data['city'])
        if form.cleaned_data.get('name'):
            doctors = doctors.filter(
                Q(user__first_name__icontains=form.cleaned_data['name']) |
                Q(user__last_name__icontains=form.cleaned_data['name'])
            )
            
    return render(request, 'medica911/client/browse_doctors.html', {
        'doctors': doctors,
        'form': form
    })

@client_required
def book_appointment(request, doctor_id):
    """Book an appointment with a doctor"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.doctor = doctor
            appointment.status = 'pending'
            appointment.save()
            messages.success(request, f"Appointment request sent to Dr. {doctor.user.get_full_name()}!")
            return redirect('client_dashboard')
    else:
        form = AppointmentForm()
    
    return render(request, 'medica911/client/book_appointment.html', {
        'form': form,
        'doctor': doctor
    })

@client_required
def add_review(request, appointment_id):
    """Add a review for a completed appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id, client=request.user, status='completed')
    if hasattr(appointment, 'review'):
        messages.info(request, "You have already reviewed this appointment.")
        return redirect('client_dashboard')
        
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.appointment = appointment
            review.save()
            
            # Update doctor overall rating
            doctor = appointment.doctor
            doctor_reviews = Review.objects.filter(appointment__doctor=doctor)
            avg_rating = doctor_reviews.aggregate(Avg('rating'))['rating__avg']
            doctor.rating = avg_rating
            doctor.total_reviews = doctor_reviews.count()
            doctor.save()

            messages.success(request, "Thank you for your review!")
            return redirect('client_dashboard')
    else:
        form = ReviewForm()
    return render(request, 'medica911/client/add_review.html', {
        'form': form,
        'appointment': appointment
    })


def doctor_detail(request, doctor_id):
    """View doctor profile details"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    reviews = Review.objects.filter(appointment__doctor=doctor)
    return render(request, 'medica911/client/doctor_detail.html', {
        'doctor': doctor,
        'reviews': reviews
    })
