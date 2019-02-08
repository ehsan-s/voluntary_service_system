from apps.accounts.models import BenefactorProfile, UserProfile
from django import forms


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'tel_number', 'address', 'activities')


class BenefactorProfileEditForm(forms.ModelForm):
    class Meta:
        model = BenefactorProfile
        fields = ('age', 'desires')
