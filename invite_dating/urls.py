from django.contrib import admin
from django.urls import path, include
from core.views import register_candidate  # 👈 Add this
from django.conf import settings
from django.conf.urls.static import static
from .views import run_setup_commands

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # 👈 ensure this is pointing to your app
    path('register/', register_candidate, name='register'),  # 👈 Add this
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



urlpatterns += [
    path('run-setup/', run_setup_commands),  # ⚠️ REMOVE THIS AFTER ONE USE
]
