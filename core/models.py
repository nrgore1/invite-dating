from django.db import models
import string
import random

def generate_unique_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

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
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    referral_code = models.OneToOneField(ReferrerCode, on_delete=models.PROTECT)
    consultant = models.ForeignKey(Consultant, on_delete=models.SET_NULL, null=True, blank=True)
    referrer = models.ForeignKey(Referrer, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class DatingUser(models.Model):
    candidate = models.OneToOneField(CandidateInquiry, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.candidate.name
