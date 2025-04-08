from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Referrer, ReferrerCode, Consultant, CandidateInquiry, DatingUser, CustomUser

# ✅ Custom User Admin with email as USERNAME_FIELD
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'is_staff', 'is_active', 'is_superuser']
    search_fields = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

# ✅ Other models
@admin.register(Referrer)
class ReferrerAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(ReferrerCode)
class ReferrerCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'referrer', 'is_used')

@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

@admin.register(CandidateInquiry)
class CandidateInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','consultant', 'referrer')
    fields = ('name', 'email', 'consultant', 'referrer')

@admin.register(DatingUser)
class DatingUserAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'age', 'gender')
