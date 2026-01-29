from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    """Decorator to restrict access to admin users only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('login')
        
        if not request.user.is_admin:
            messages.error(request, 'Admin access required.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def doctor_required(view_func):
    """Decorator to restrict access to doctor users only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('login')
        
        # Allow superusers or users with doctor role
        if not (request.user.is_doctor or request.user.is_superuser):
            messages.error(request, 'Doctor access required.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def client_required(view_func):
    """Decorator to restrict access to client users only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('login')
        
        # Allow superusers or users with client role
        if not (request.user.is_client or request.user.is_superuser):
            messages.error(request, 'Client access required.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper
