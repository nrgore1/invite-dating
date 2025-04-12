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

class DatingProfileForm(forms.ModelForm):
    class Meta:
        model = DatingUser
        fields = ['photo', 'bio', 'interests', 'age', 'gender', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'interests': forms.Textarea(attrs={'rows': 2}),
            'age': forms.NumberInput(attrs={'min': 18}),
            'gender': forms.TextInput(attrs={'placeholder': 'e.g., Male/Female/Other'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, State'}),
        }


# ✅ Form for referrer registration
class ReferrerForm(forms.ModelForm):
    class Meta:
        model = Referrer
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Referrer Email'}),
        }
