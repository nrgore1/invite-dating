from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
import string
import random


# Utility to generate unique referral codes
def generate_unique_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# Custom user model
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Consultant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Referrer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class ReferrerCode(models.Model):
    code = models.CharField(max_length=10, unique=True, default=generate_unique_code)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    referrer = models.ForeignKey(Referrer, on_delete=models.CASCADE, related_name='codes')
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} ({'Used' if self.is_used else 'Unused'})"



class CandidateInquiry(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    referrer_code = models.ForeignKey(ReferrerCode, on_delete=models.SET_NULL, null=True, blank=True)
    consultant = models.ForeignKey(Consultant, on_delete=models.SET_NULL, null=True, blank=True)
    referrer = models.ForeignKey(Referrer, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name or self.email


class DatingUser(models.Model):
    candidate = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dating_profile")
    bio = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    referrer_code = models.ForeignKey(ReferrerCode, on_delete=models.SET_NULL, null=True, blank=True)  # ✅ Add this line

    def __str__(self):
        return self.candidate.email

