# admin.py
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path
from django.utils.html import format_html
from django.template.response import TemplateResponse
from .models import ReferrerProfile, ReferrerCode, DatingUser

@admin.register(ReferrerProfile)
class ReferrerProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'total_codes', 'used_codes', 'unused_codes', 'generate_referral_codes_link']
    search_fields = ['name', 'email']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:referrer_id>/generate-codes/',
                self.admin_site.admin_view(self.generate_referral_codes_view),
                name='generate_referral_codes',
            ),
        ]
        return custom_urls + urls

    def generate_referral_codes_link(self, obj):
        return format_html(
            '<a class="button" href="{}">Generate Referral Codes</a>',
            f"{obj.id}/generate-codes/"
        )
    generate_referral_codes_link.short_description = 'Referral Codes'

    def generate_referral_codes_view(self, request, referrer_id):
        referrer = ReferrerProfile.objects.get(pk=referrer_id)

        if request.method == "POST":
            count = int(request.POST.get("count", 1))
            for _ in range(count):
                ReferrerCode.objects.create(referrer=referrer)
            self.message_user(request, f"✅ Created {count} referral code(s) for {referrer.name}.", messages.SUCCESS)
            return redirect(f"/admin/core/referrerprofile/{referrer_id}/change/")

        return TemplateResponse(request, "admin/generate_codes.html", context={
            "referrer": referrer,
            "title": f"Generate Referral Codes for {referrer.name}"
        })

    def total_codes(self, obj):
        return obj.referral_codes.count()

    def used_codes(self, obj):
        return obj.referral_codes.filter(used=True).count()

    def unused_codes(self, obj):
        return obj.referral_codes.filter(used=False).count()


class ReferrerCodeAdmin(admin.ModelAdmin):
    list_display = ['referrer', 'referral_code', 'used', 'created_at']
    readonly_fields = ['referral_code', 'created_at']
    list_filter = ['used', 'created_at']
    search_fields = ['referral_code', 'referrer__name']


admin.site.register(ReferrerCode, ReferrerCodeAdmin)


@admin.register(DatingUser)
class DatingUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'referral_code']
    search_fields = ['user__username', 'referral_code__referral_code']
