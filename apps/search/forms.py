from django import forms
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator


class benefactorNonFinancialForm(forms.Form):
    city = forms.CharField(max_length=100, required=False)
    gender = forms.CharField(max_length=20, required=False)
    org_username = forms.CharField(max_length=100, required=False)
    project_name = forms.CharField(max_length=100, required=False)


class organizationNonFinancialForm(forms.Form):
    city = forms.CharField(max_length=100, required=False)
    gender = forms.CharField(max_length=20, required=True)
    benefactor_username = forms.CharField(max_length=100, required=False)

