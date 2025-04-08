from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register/', views.register_candidate, name='register'),
    path('register-referrer/', views.register_referrer, name='register_referrer'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('profile-preview/', views.profile_preview, name='profile_preview'),
    path('inquiry/', views.candidate_inquiry, name='candidate_inquiry'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('home/', views.home, name='home'),
]
