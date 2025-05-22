from . import views
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import register_referrer
from .views import home, candidate_inquiry, thank_you, register_candidate, create_profile, profile_preview
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_candidate, name='register'),
    path('register-referrer/', views.register_referrer, name='register_referrer'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('profile-preview/', views.profile_preview, name='profile_preview'),
    path('inquiry/', views.candidate_inquiry, name='candidate_inquiry'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),  # ✅ ensure this is used
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('', views.landing_page, name='landing_page'),

]
from django.contrib.auth.views import LogoutView

path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),

# from .views import create_superuser_view

# urlpatterns += [
#   path('create-superuser/', create_superuser_view, name='create_superuser'),
# ]
   

from .views import referrer_dashboard, consultant_dashboard

urlpatterns += [
    path('referrer-dashboard/', referrer_dashboard, name='referrer_dashboard'),
    path('consultant-dashboard/', consultant_dashboard, name='consultant_dashboard'),
]
from core.views import CustomLoginView
