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


@admin.register(Referrer)
class ReferrerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name', 'email']


@admin.register(ReferrerCode)
class ReferrerCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'referrer', 'is_used')
    list_filter = ['is_used']
    search_fields = ['code', 'referrer__first_name', 'referrer__last_name']


@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ['first_name', 'last_name', 'email']


@admin.register(CandidateInquiry)
class CandidateInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'consultant', 'referrer')
    fields = ('name', 'email', 'consultant', 'referrer')
    search_fields = ['name', 'email']


@admin.register(DatingUser)
class DatingUserAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'first_name', 'last_name', 'age', 'gender', 'is_approved', 'referrer_code')
    list_filter = ['is_approved', 'gender']
    search_fields = ['candidate__email', 'first_name', 'last_name']
    actions = ['approve_selected_users']

    @admin.action(description='✅ Approve and send email')
    def approve_selected_users(self, request, queryset):
        from .views import send_approval_email
        for user in queryset:
            if not user.is_approved:
                user.is_approved = True
                user.save()
                send_approval_email(user)
