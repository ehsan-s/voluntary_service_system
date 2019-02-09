from django import forms
from apps.project.models import FinancialProject, NonFinancialProject


class FinancialProjectForm(forms.ModelForm):

    class Meta:
        model = FinancialProject
        fields = ('deadline', 'money_needed', 'name')


class NonFinancialProjectForm(forms.ModelForm):

    class Meta:
        model = NonFinancialProject
        fields = ('age', 'gender', 'location', 'name')
