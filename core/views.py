from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.urls import reverse
from django.contrib import messages
from .forms import ReferrerForm


from .models import ReferrerCode, DatingUser, CandidateInquiry, Consultant
from .forms import CandidateInquiryForm, DatingProfileForm


def register_candidate(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        code = request.POST['referral_code']

        try:
            referral = ReferrerCode.objects.get(referral_code=code)
            if DatingUser.objects.filter(referral_code=referral).exists():
                return HttpResponseBadRequest("Referral code already used.")

            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            DatingUser.objects.create(user=user, referral_code=referral)

            # Auto login
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

            # Email
            profile_link = request.build_absolute_uri(reverse('create_profile'))
            send_mail(
                subject="🎉 Welcome to Invite-Only Dating!",
                message=f"Hi {username},\n\nYour registration is confirmed!\nCreate your profile: {profile_link}",
                from_email="ng66india@gmail.com",
                recipient_list=[email],
                fail_silently=False,
            )

            return redirect('create_profile')
        except ReferrerCode.DoesNotExist:
            return HttpResponseBadRequest("Invalid referral code.")

    return render(request, 'register.html')


@login_required
def create_profile(request):
    try:
        profile = request.user.dating_profile
    except DatingUser.DoesNotExist:
        return HttpResponseNotFound("Profile does not exist. Contact support.")

    if request.method == 'POST':
        form = DatingProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile saved successfully.")
            return redirect('profile_preview')
    else:
        form = DatingProfileForm(instance=profile)

    return render(request, 'create_profile.html', {'form': form})


@login_required
def profile_preview(request):
    try:
        profile = request.user.dating_profile
    except DatingUser.DoesNotExist:
        return HttpResponseNotFound("❌ You have not created a dating profile yet. Please <a href='/create-profile/'>create your profile</a>.")

    return render(request, 'profile_preview.html', {'profile': profile})

from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

from django.shortcuts import render

def candidate_inquiry(request):
    return render(request, 'core/inquiry.html')

from django.shortcuts import render

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
