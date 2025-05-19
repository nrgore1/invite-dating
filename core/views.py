from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.urls import reverse
from django.contrib import messages
from .forms import ReferrerForm, CandidateInquiryForm, DatingProfileForm
from .models import ReferrerCode, CandidateInquiry, DatingUser, Consultant
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.contrib.admin.views.decorators import staff_member_required

User = get_user_model()

def register_candidate(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        referral_code = request.POST.get("referral_code")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return render(request, "registration/register.html")

        # ✅ Get referral instance
        referral = get_object_or_404(ReferrerCode, code=referral_code)

        # ✅ Create user and login
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)  # 👈 Auto-login

        # ✅ Save inquiry and link to user
        inquiry = CandidateInquiry.objects.create(
            name=username,  # Or get from form
            email=email,
            referral_code=referral,
        )
        DatingUser.objects.create(candidate=inquiry, user=user)

        return redirect("create_profile")  # 👈 Redirect to profile creation

    return render(request, "registration/register.html")


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
        return HttpResponseNotFound(
            "❌ You have not created a dating profile yet. Please <a href='/create-profile/'>create your profile</a>."
        )

    return render(request, 'profile_preview.html', {'profile': profile})

def home(request):
    return render(request, 'core/home.html')

def candidate_inquiry(request):
    return render(request, 'core/inquiry.html')

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
    return render(request, 'inquiry.html')  # ✅ use the actual file name

# def landing_page(request):
#    return render(request, 'core/landing_page.html')
def landing_page(request):
    return render(request, 'landing_page.html')

from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing_page.html')



# @staff_member_required
# def run_setup_commands(request):
def run_setup_commands(request):
    call_command('migrate')
    call_command('collectstatic', '--noinput')
    return HttpResponse("Migrations and static collection done.")
