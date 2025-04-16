from django import forms
from .models import CandidateInquiry, DatingUser, Referrer

# ✅ Candidate inquiry form
class CandidateInquiryForm(forms.ModelForm):
    class Meta:
        model = CandidateInquiry
        fields = ['name', 'email', 'phone', 'consultant', 'referrer']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone (optional)'}),
        }

# ✅ Referrer form
class ReferrerForm(forms.ModelForm):
    class Meta:
        model = Referrer
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
        }

# ✅ Step 1: Basic Info
class DatingProfileStep1Form(forms.ModelForm):
    class Meta:
        model = DatingUser
        fields = ['age', 'gender', 'location']
        widgets = {
            'age': forms.NumberInput(attrs={'min': 18, 'placeholder': 'Your Age'}),
            'gender': forms.TextInput(attrs={'placeholder': 'e.g., Male/Female/Other'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, State'}),
        }

# ✅ Step 2: About You
class DatingProfileStep2Form(forms.ModelForm):
    class Meta:
        model = DatingUser
        fields = ['bio', 'interests']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself'}),
            'interests': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Hobbies, passions...'}),
        }

# ✅ Step 3: Photo Upload
class DatingProfileStep3Form(forms.ModelForm):
    class Meta:
        model = DatingUser
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(),
        }

# ✅ Full Profile Form (for fallback or admin)
class DatingProfileForm(forms.ModelForm):
    class Meta:
        model = DatingUser
        fields = ['age', 'gender', 'location', 'bio', 'interests', 'photo']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself'}),
            'interests': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Hobbies, passions...'}),
            'age': forms.NumberInput(attrs={'min': 18}),
            'gender': forms.TextInput(attrs={'placeholder': 'e.g., Male/Female/Other'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, State'}),
        }
