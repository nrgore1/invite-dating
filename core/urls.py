from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from core.views import (
    landing_page, home, register_candidate, register_referrer, create_profile,
    profile_preview, candidate_inquiry, thank_you, run_setup_commands,
    CustomLoginView, referrer_dashboard, consultant_dashboard
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('home/', home, name='home'),
    path('register/', register_candidate, name='register'),
    path('register-referrer/', register_referrer, name='register_referrer'),
    path('create-profile/', create_profile, name='create_profile'),
    path('profile-preview/', profile_preview, name='profile_preview'),
    path('inquiry/', candidate_inquiry, name='candidate_inquiry'),
    path('thank-you/', thank_you, name='thank_you'),
    path('run-setup/', run_setup_commands),  # optional: remove after setup
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('referrer-dashboard/', referrer_dashboard, name='referrer_dashboard'),
    path('consultant-dashboard/', consultant_dashboard, name='consultant_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
