from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def role_required(allowed_roles):
    """Decorator to restrict access based on user role"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Please login to access this page.')
                return redirect('login')
            
            if request.user.role not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_required(view_func):
    """Decorator to restrict access to admin users only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('login')
        
        if request.user.role != 'admin':
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
        
        if request.user.role != 'doctor':
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
        
        if request.user.role != 'client':
            messages.error(request, 'Client access required.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper
