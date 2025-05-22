from django.contrib import admin
from django.urls import path, include
from core.views import register_candidate  # 👈 Add this
from django.conf import settings
from django.conf.urls.static import static
from core.views import run_setup_commands
from .views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # 👈 ensure this is pointing to your app
    path('register/', register_candidate, name='register'),  # 👈 Add this
    path('run-setup/', run_setup_commands),  # ⚠️ REMOVE THIS AFTER ONE USE
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    # ... all your other routes
]