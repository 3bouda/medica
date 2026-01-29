from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_field
from .models import Doctor
import logging

logger = logging.getLogger(__name__)

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Already linked?
        if sociallogin.is_existing:
            return

        # Check if user already exists with this email
        from django.contrib.auth import get_user_model
        User = get_user_model()
        email = sociallogin.user.email
        if email:
            try:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
                
                # If they wanted to be a doctor but are currently a client, update them
                selected_role = request.session.get('selected_role')
                if selected_role == 'doctor' and user.role == 'client':
                    user.role = 'doctor'
                    user.save()
                    if not Doctor.objects.filter(user=user).exists():
                        Doctor.objects.create(
                            user=user, 
                            license_number=f"GOOGLE-UPGRADE-{user.id}"
                        )
            except User.DoesNotExist:
                pass

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        
        # Capture role from session (set in signup_view)
        selected_role = request.session.get('selected_role')
        
        # In our model, role defaults to 'client', so it's never empty.
        # If the session specifically says 'doctor', we must apply it.
        if selected_role == 'doctor':
            user.role = 'doctor'
            user.save()
        elif not user.role:
            user.role = 'client'
            user.save()
            
        # If the user is a doctor, ensure they have a profile
        if user.role == 'doctor':
            if not Doctor.objects.filter(user=user).exists():
                Doctor.objects.create(
                    user=user, 
                    license_number=f"GOOGLE-PENDING-{user.id}"
                )
        
        return user

    def is_auto_signup_allowed(self, request, sociallogin):
        # Always allow auto-signup to bypass the 3rd party signup page
        return True
