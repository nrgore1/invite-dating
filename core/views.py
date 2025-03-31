from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import ReferralCode, DatingUser
from django.http import HttpResponseBadRequest

def register_candidate(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        code = request.POST['referral_code']

        try:
            referral = ReferralCode.objects.get(code=code)
            if DatingUser.objects.filter(referral_code=referral).exists():
                return HttpResponseBadRequest("Referral code already used.")
            
            user = User.objects.create_user(username=username, password=password)
            DatingUser.objects.create(user=user, referral_code=referral)
            return redirect('/admin/')  # Redirect to success or login
        except ReferralCode.DoesNotExist:
            return HttpResponseBadRequest("Invalid referral code.")

    return render(request, 'register.html')
