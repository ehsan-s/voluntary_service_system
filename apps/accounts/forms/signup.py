from django.contrib.auth.forms import UserCreationForm
from apps.accounts.models import OrganizationProfile, BenefactorProfile, UserProfile, User
from django import forms
from django.core.validators import RegexValidator, EmailValidator
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class BenefactorUserSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email_validator = EmailValidator(message=_("Please enter your email correctly"))
    email = forms.CharField(validators=[email_validator], max_length=50, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

    def clean_email(self):
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError('Email is registered')
        return email

    def save(self, commit=True):
        user = super(BenefactorUserSignupForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class UserProfileSignupForm(forms.ModelForm):
    phone_regex = RegexValidator(regex=r'^\d{8,15}$', message=_("Please enter your phone number correctly!"))
    phone_number = forms.CharField(validators=[phone_regex])
    tel_regex = RegexValidator(regex=r'^\d{8,15}$', message=_("Please enter your phone number correctly!"))
    tel_number = forms.CharField(validators=[tel_regex])
    address = forms.CharField(max_length=200, required=True)

    class Meta:
        model = UserProfile
        fields = ('phone_number', 'tel_number', 'address', 'activities')


class BenefactorSignUpForm(forms.ModelForm):

    class Meta:
        model = BenefactorProfile
        fields = ('age', 'desires')


class OrgUserSignupForm(UserCreationForm):
    email_validator = EmailValidator(message=_("Please enter your email correctly"))
    email = forms.CharField(validators=[email_validator], max_length=50, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def clean_email(self):
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError('Email is registered')
        return email

    def save(self, commit=True):
        user = super(OrgUserSignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class OrgSignUpForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        fields = ('name', )

