from django.contrib import admin
from django.urls import path, include
from core.views import (
    register_candidate,
    run_setup_commands,
    create_superuser_view,
    CustomLoginView,
    referrer_dashboard,
    consultant_dashboard,
)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_candidate, name='register'),
    path('run-setup/', run_setup_commands),
    path('create-superuser/', create_superuser_view),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('referrer-dashboard/', referrer_dashboard, name='referrer_dashboard'),
    path('consultant-dashboard/', consultant_dashboard, name='consultant_dashboard'),
    path('', include('core.urls')),  # All other app routes
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
