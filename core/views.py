from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model

from .forms import (
    ReferrerForm,
    CandidateInquiryForm,
    DatingProfileForm,
    DatingProfileStep1Form,
    DatingProfileStep2Form,
    DatingProfileStep3Form,
)
from .models import ReferrerCode, CandidateInquiry, DatingUser, Consultant

User = get_user_model()

# ✅ Email sender used by admin approval action
def send_approval_email(dating_user):
    ref_code = dating_user.referrer_code.code if dating_user.referrer_code else 'N/A'
    profile_url = reverse('create_profile')
    full_url = f"https://invite-dating.onrender.com{profile_url}"

    subject = "You're approved! Create your dating profile 💖"
    message = f"""
Hi {dating_user.first_name},

You've been approved to create your dating profile on InviteDating!

👉 Here is your unique code for creating your profile: {ref_code}
🕒 This code can only be used once and will expire after your profile is created.

Click the link below to begin:
{full_url}

See you soon,  
InviteDating Team
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[dating_user.candidate.email],
        fail_silently=False,
    )


# ✅ Candidate registration
def register_candidate(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('referral_code')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if not all([email, password, code, first_name, last_name]):
            messages.error(request, "All fields are required.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with that email already exists. Please log in or use a different email.")
            return redirect('register')

        try:
            referral = ReferrerCode.objects.get(code=code)

            if DatingUser.objects.filter(referrer_code=referral).exists():
                messages.error(request, "This referral code has already been used.")
                return redirect('register')

            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            DatingUser.objects.create(
                candidate=user,
                first_name=first_name,
                last_name=last_name,
                referrer_code=referral
            )

            messages.success(request, "Registration successful! Await admin approval before creating your profile.")
            return redirect('home')

        except ReferrerCode.DoesNotExist:
            messages.error(request, "Invalid referral code.")
            return redirect('register')

    return render(request, 'core/register.html')


# ✅ Multi-step Profile Wizard

# Step 1: Basic Info
@login_required
def profile_step1(request):
    profile = request.user.dating_profile

    if not profile.is_approved:
        return HttpResponseForbidden("⏳ Awaiting admin approval.")

    if request.method == 'POST':
        form = DatingProfileStep1Form(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_step2')
    else:
        form = DatingProfileStep1Form(instance=profile)

    return render(request, 'core/profile_step1.html', {'form': form, 'step': 1})


# Step 2: About You
@login_required
def profile_step2(request):
    profile = request.user.dating_profile

    if not profile.is_approved:
        return HttpResponseForbidden("⏳ Awaiting admin approval.")

    if request.method == 'POST':
        form = DatingProfileStep2Form(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_step3')
    else:
        form = DatingProfileStep2Form(instance=profile)

    return render(request, 'core/profile_step2.html', {'form': form, 'step': 2})


# Step 3: Photo Upload + Finalize
@login_required
def profile_step3(request):
    profile = request.user.dating_profile

    if not profile.is_approved:
        return HttpResponseForbidden("⏳ Awaiting admin approval.")

    if profile.referrer_code and profile.referrer_code.is_used:
        return HttpResponse("❌ This referral code has already been used.")

    if request.method == 'POST':
        form = DatingProfileStep3Form(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            if profile.referrer_code:
                profile.referrer_code.is_used = True
                profile.referrer_code.save()

            messages.success(request, "✅ Your profile has been created!")
            return redirect('profile_preview')
    else:
        form = DatingProfileStep3Form(instance=profile)

    return render(request, 'core/profile_step3.html', {'form': form, 'step': 3})


# ✅ Classic single-page profile creation fallback
@login_required
def create_profile(request):
    user = request.user
    try:
        profile = user.dating_profile
    except DatingUser.DoesNotExist:
        return HttpResponseNotFound("You have not registered yet.")

    if not profile.is_approved:
        return HttpResponseForbidden("⏳ Your account is pending approval.")

    if profile.referrer_code and profile.referrer_code.is_used:
        return HttpResponse("❌ Referral code already used.")

    if request.method == 'POST':
        form = DatingProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            if profile.referrer_code:
                profile.referrer_code.is_used = True
                profile.referrer_code.save()
            messages.success(request, "✅ Your profile has been created!")
            return redirect('profile_preview')
    else:
        form = DatingProfileForm(instance=profile)

    return render(request, 'core/create_profile.html', {'form': form})


# ✅ Profile preview
@login_required
def profile_preview(request):
    try:
        profile = request.user.dating_profile
    except DatingUser.DoesNotExist:
        return HttpResponseNotFound(
            "❌ You have not created a dating profile yet. Please <a href='/create-profile/'>create your profile</a>."
        )

    return render(request, 'profile_preview.html', {'profile': profile})


# ✅ Smart login redirect
@login_required
def post_login_redirect(request):
    try:
        profile = request.user.dating_profile
    except DatingUser.DoesNotExist:
        return redirect('register')

    if not profile.is_approved:
        messages.info(request, "⏳ Your profile is pending approval.")
        return redirect('home')

    if not profile.photo:
        return redirect('profile_step1')

    return redirect('profile_preview')


# ✅ Public Views
def home(request):
    return render(request, 'core/home.html')

def thank_you(request):
    return render(request, 'core/thank_you.html')

def register_referrer(request):
    if request.method == 'POST':
        form = ReferrerForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'thank_you.html', {'message': 'Thank you for registering as a referrer!'})
    else:
        form = ReferrerForm()
    return render(request, 'register_referrer.html', {'form': form})

def candidate_inquiry(request):
    return render(request, 'inquiry.html')

def landing_page(request):
    return render(request, 'landing_page.html')
