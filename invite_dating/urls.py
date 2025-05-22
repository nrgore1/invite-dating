from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import (
    register_candidate,
    run_setup_commands,
    CustomLoginView,
    referrer_dashboard,
    consultant_dashboard,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Core app URLs
    path('register/', register_candidate, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('referrer-dashboard/', referrer_dashboard, name='referrer_dashboard'),
    path('consultant-dashboard/', consultant_dashboard, name='consultant_dashboard'),

    # ✅ Temporary: for first-time setup only (delete after one use)
    path('run-setup/', run_setup_commands),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
