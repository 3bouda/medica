from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Shared
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # Admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/<str:role>/', views.manage_users, name='manage_users'),
    
    # Doctor
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/profile/edit/', views.doctor_profile_edit, name='doctor_profile_edit'),
    path('doctor/appointment/<int:pk>/update/', views.update_appointment, name='update_appointment'),
    
    # Client
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
    path('doctors/browse/', views.browse_doctors, name='browse_doctors'),
    path('doctors/<int:doctor_id>/book/', views.book_appointment, name='book_appointment'),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('appointment/<int:appointment_id>/review/', views.add_review, name='add_review'),
]
