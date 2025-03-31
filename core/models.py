from django.db import models
from django.contrib.auth.models import User
from .utils import generate_unique_code


class ReferrerProfile(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, default='placeholder@example.com')

    def __str__(self):
        return self.name


class ReferrerCode(models.Model):
    referrer = models.ForeignKey(ReferrerProfile, on_delete=models.CASCADE, related_name='referral_codes')
    referral_code = models.CharField(max_length=10, unique=True, blank=True)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = generate_unique_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.referral_code or '[NO CODE]'} - {self.referrer.name}"


class DatingUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dating_profile')
    referral_code = models.OneToOneField(ReferrerCode, on_delete=models.PROTECT)

    def __str__(self):
        return f"DatingUser: {self.user.username}"
