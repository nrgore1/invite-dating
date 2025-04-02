
from django import forms
from .models import CandidateInquiry

class CandidateInquiryForm(forms.ModelForm):
    class Meta:
        model = CandidateInquiry
        fields = ['name', 'email', 'phone', 'referral_code', 'consultant', 'referrer']

from .models import DatingUser

class DatingProfileForm(forms.ModelForm):
    class Meta:
        model = DatingUser
        fields = ['bio', 'age', 'location', 'interests', 'photo']
        
from .models import Referrer

class ReferrerForm(forms.ModelForm):
    class Meta:
        model = Referrer
        fields = ['name', 'email']
