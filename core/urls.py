from django.urls import path
from .views import register_referrer
from .views import home, candidate_inquiry, thank_you, register_candidate, create_profile, profile_preview

urlpatterns = [
    path('', home, name='home'),
    path('inquiry/', candidate_inquiry, name='candidate_inquiry'),
    path('thanks/', thank_you, name='thanks'),
    path('register/', register_candidate, name='register_candidate'),
    path('create-profile/', create_profile, name='create_profile'),
    path('profile-preview/', profile_preview, name='profile_preview'),
]

urlpatterns += [
    path('create-profile/', create_profile, name='create_profile'),
]

urlpatterns = [
    path('register-referrer/', register_referrer, name='register_referrer'),
    # other paths...
]

