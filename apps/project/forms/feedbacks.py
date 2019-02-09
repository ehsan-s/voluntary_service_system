from django import forms
from apps.project.models import Feedback


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ('rate', 'feedback', 'feeder')
