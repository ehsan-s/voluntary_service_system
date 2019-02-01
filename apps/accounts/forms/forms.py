from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    age = forms.IntegerField(required=False)
    phone_regex = RegexValidator(regex=r'^\d{8,15}$', message=_("Please enter your phone number correctly!"))
    phone_number = forms.CharField(validators=[phone_regex], required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'age', 'phone_number', 'email', 'password1', 'password2')