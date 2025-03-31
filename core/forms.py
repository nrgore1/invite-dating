from django import forms
from .models import ReferrerCode
from .utils import generate_unique_code

class ReferrerCodeForm(forms.ModelForm):
    class Meta:
        model = ReferrerCode
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.referral_code:
            instance.referral_code = generate_unique_code()
        if commit:
            instance.save()
        return instance
