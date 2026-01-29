from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Doctor, Appointment, Review, Speciality, DoctorAvailability


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'
        })
    )
    role = forms.ChoiceField(
        choices=[('client', 'Client'), ('doctor', 'Doctor')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'role', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


class CustomLoginForm(AuthenticationForm):
    """Custom login form"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'date_of_birth', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profile_picture': forms.URLInput(attrs={'class': 'form-control'}),
        }


class DoctorProfileForm(forms.ModelForm):
    """Form for updating doctor profile"""
    
    class Meta:
        model = Doctor
        fields = ['speciality', 'license_number', 'experience_years', 'consultation_fee', 
                  'bio', 'education', 'clinic_name', 'clinic_address', 'is_available']
        widgets = {
            'speciality': forms.Select(attrs={'class': 'form-select'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'clinic_name': forms.TextInput(attrs={'class': 'form-control'}),
            'clinic_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DoctorRegistrationForm(forms.ModelForm):
    """Form for doctor registration details"""
    
    class Meta:
        model = Doctor
        fields = ['speciality', 'license_number', 'experience_years', 'consultation_fee', 'clinic_name', 'clinic_address']
        widgets = {
            'speciality': forms.Select(attrs={'class': 'form-select'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Medical License Number'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of Experience'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Consultation Fee'}),
            'clinic_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clinic Name'}),
            'clinic_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Clinic Address'}),
        }


class AppointmentForm(forms.ModelForm):
    """Form for booking appointments"""
    
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'reason']
        widgets = {
            'appointment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'appointment_time': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your symptoms or reason for visit'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generate time slots
        time_choices = []
        for hour in range(8, 18):  # 8 AM to 6 PM
            for minute in ['00', '30']:
                time_str = f"{hour:02d}:{minute}"
                time_choices.append((time_str, f"{hour:02d}:{minute}"))
        self.fields['appointment_time'] = forms.ChoiceField(
            choices=time_choices,
            widget=forms.Select(attrs={'class': 'form-select'})
        )


class AppointmentUpdateForm(forms.ModelForm):
    """Form for updating appointment status"""
    
    class Meta:
        model = Appointment
        fields = ['status', 'notes', 'diagnosis', 'prescription']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prescription': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ReviewForm(forms.ModelForm):
    """Form for submitting reviews"""
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} ⭐') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience...'
            }),
        }


class DoctorAvailabilityForm(forms.ModelForm):
    """Form for setting doctor availability"""
    
    class Meta:
        model = DoctorAvailability
        fields = ['day_of_week', 'start_time', 'end_time', 'is_active']
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DoctorSearchForm(forms.Form):
    """Form for searching doctors"""
    
    speciality = forms.ModelChoiceField(
        queryset=Speciality.objects.all(),
        required=False,
        empty_label="All Specialities",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City or Location'
        })
    )
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Doctor Name'
        })
    )


class AppointmentFilterForm(forms.Form):
    """Form for filtering appointments"""
    
    STATUS_CHOICES = [('', 'All Status')] + list(Appointment.STATUS_CHOICES)
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    speciality = forms.ModelChoiceField(
        queryset=Speciality.objects.all(),
        required=False,
        empty_label="All Specialities",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
