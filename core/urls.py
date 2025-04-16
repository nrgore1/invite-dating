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
    path('post-login/', views.post_login_redirect, name='post_login_redirect'),
    path('profile/step1/', views.profile_step1, name='profile_step1'),
    path('profile/step2/', views.profile_step2, name='profile_step2'),
    path('profile/step3/', views.profile_step3, name='profile_step3'),
]
