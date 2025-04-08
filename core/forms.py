from django import forms
from .models import CandidateInquiry, DatingUser, Referrer

# ✅ Form for candidate inquiry
class CandidateInquiryForm(forms.ModelForm):
    class Meta:
        model = CandidateInquiry
        fields = ['name', 'email', 'phone', 'consultant', 'referrer']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone (optional)'}),
        }

# ✅ Form for dating profile
class DatingProfileForm(forms.ModelForm):
    class Meta:
        model = DatingUser
        fields = ['bio', 'age', 'location', 'interests', 'photo']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself'}),
            'interests': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Hobbies, passions...'}),
        }

# ✅ Form for referrer registration
class ReferrerForm(forms.ModelForm):
    class Meta:
        model = Referrer
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Referrer Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Referrer Email'}),
        }
