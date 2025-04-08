from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.urls import reverse
from django.contrib import messages

from .forms import ReferrerForm, CandidateInquiryForm, DatingProfileForm
from .models import ReferrerCode, CandidateInquiry, DatingUser, Consultant
from django.contrib.auth import get_user_model

User = get_user_model()


def register_candidate(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('referral_code')

        if not email or not password or not code:
            messages.error(request, "All fields are required.")
            return redirect('register')

        full_name = email.split('@')[0]

        try:
            referral = ReferrerCode.objects.get(code=code)

            # FIXED FIELD NAME
            if DatingUser.objects.filter(referrer_code=referral).exists():
                messages.error(request, "This referral code has already been used.")
                return redirect('register')

            user = User.objects.create_user(email=email, password=password, first_name=full_name)
            DatingUser.objects.create(candidate=user)


            messages.success(request, "Registration successful! You can now create your profile.")
            return redirect('create_profile')

        except ReferrerCode.DoesNotExist:
            messages.error(request, "Invalid referral code. Please check and try again.")
            return redirect('register')

    return render(request, 'core/register.html')



@login_required
def profile_preview(request):
    try:
        profile = request.user.dating_profile
    except DatingUser.DoesNotExist:
        return HttpResponseNotFound(
            "❌ You have not created a dating profile yet. Please <a href='/create-profile/'>create your profile</a>."
        )

    return render(request, 'profile_preview.html', {'profile': profile})


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


def create_profile(request):
    return HttpResponse("Profile creation coming soon!")
