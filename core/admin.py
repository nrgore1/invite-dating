from django.contrib import admin
from .models import Referrer, ReferrerCode, Consultant, CandidateInquiry, DatingUser

@admin.register(Referrer)
class ReferrerAdmin(admin.ModelAdmin):
    list_display = ['name']  # customize as needed

@admin.register(ReferrerCode)
class ReferrerCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'referrer', 'is_used')

@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

@admin.register(CandidateInquiry)
class CandidateInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'referral_code', 'consultant', 'referrer')
    fields = ('name', 'email', 'referral_code', 'consultant', 'referrer')  # 👈 Add this

@admin.register(DatingUser)
class DatingUserAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'age', 'gender')


from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(CustomUser, UserAdmin)

