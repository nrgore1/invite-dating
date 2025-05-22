from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.contrib import messages
from .forms import ReferrerForm, CandidateInquiryForm, DatingProfileForm
from .models import ReferrerCode, CandidateInquiry, DatingUser, Consultant
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView

User = get_user_model()

def landing_page(request):
    return render(request, 'landing_page.html')

def home(request):
    return render(request, 'core/home.html')

def register_candidate(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        referral_code = request.POST.get("referral_code")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "registration/register.html")

        referral = get_object_or_404(ReferrerCode, code=referral_code)
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)

        inquiry = CandidateInquiry.objects.create(name=username, email=email, referral_code=referral)
        DatingUser.objects.create(candidate=user)

        return redirect("create_profile")

    return render(request, "registration/register.html")

@login_required
def create_profile(request):
    try:
        profile = request.user.dating_profile
    except DatingUser.DoesNotExist:
        return HttpResponseNotFound("Profile does not exist. Contact support.")

    form = DatingProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Profile saved.")
        return redirect('profile_preview')

    return render(request, 'create_profile.html', {'form': form})

@login_required
def profile_preview(request):
    try:
        profile = request.user.dating_profile
    except DatingUser.DoesNotExist:
        return HttpResponseNotFound("Profile not found. Please <a href='/create-profile/'>create one</a>.")

    return render(request, 'profile_preview.html', {'profile': profile})

def thank_you(request):
    return render(request, 'core/thank_you.html')

def register_referrer(request):
    form = ReferrerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return render(request, 'thank_you.html', {'message': 'Thank you for registering!'})
    return render(request, 'register_referrer.html', {'form': form})

def candidate_inquiry(request):
    return render(request, 'inquiry.html')

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user

        if hasattr(user, 'dating_profile'):
            return reverse('matches')
        if user.groups.filter(name='Referrers').exists():
            return reverse('referrer_dashboard')
        if user.groups.filter(name='Consultants').exists():
            return reverse('consultant_dashboard')
        if hasattr(user, 'datinguser'):
            return reverse('create_profile')

        return reverse('landing_page')

@login_required
def referrer_dashboard(request):
    return render(request, "referrer_dashboard.html")

@staff_member_required
def consultant_dashboard(request):
    return render(request, "consultant_dashboard.html")

@login_required
def matches(request):
    # Stub match view
    return render(request, "matches.html")
