from django.views.generic.edit import CreateView
from apps.accounts.forms.forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = '/nemidunam'
    template_name = 'accounts/profile/signup.html'

