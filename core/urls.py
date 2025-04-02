from . import views
from django.urls import path
from .views import register_referrer
from .views import home, candidate_inquiry, thank_you, register_candidate, create_profile, profile_preview

urlpatterns = [
    path('', views.home, name='home'),  # 👈 fixes the "home" route
    path('register-referrer/', views.register_referrer, name='register_referrer'),
    path('register/', views.register_candidate, name='register_candidate'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('profile-preview/', views.profile_preview, name='profile_preview'),
     path('inquiry/', views.candidate_inquiry, name='candidate_inquiry'),
]

urlpatterns += [
    path('create-profile/', create_profile, name='create_profile'),
]



