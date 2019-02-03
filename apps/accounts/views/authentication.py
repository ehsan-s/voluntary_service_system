from django.views.decorators.csrf import csrf_exempt
from apps.accounts.forms import BenefactorSignUpForm, UserProfileSignupForm, BenefactorUserSignupForm, \
    OrgUserSignupForm, OrgSignUpForm
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

@csrf_exempt
def register_benefactor(request):
    if request.method == "POST":
        print(request.POST)
        user_form = BenefactorUserSignupForm(request.POST)
        user_profile_form = UserProfileSignupForm(request.POST)
        benefactor_form = BenefactorSignUpForm(request.POST)
        if user_form.is_valid():
            if user_profile_form.is_valid():
                if benefactor_form.is_valid():
                    user = user_form.save()
                    user_profile = user_profile_form.save(commit=False)
                    user_profile.user = user
                    user_profile.save()
                    benefactor_form = benefactor_form.save(commit=False)
                    benefactor_form.profile = user_profile
                    benefactor_form.save()
                    return JsonResponse({'status': '0'})
                else:
                    return JsonResponse({'status': '-1', 'message': dict(benefactor_form.errors.items())})
            else:
                return JsonResponse({'status': '-1', 'message': dict(user_profile_form.errors.items())})
        else:
            return JsonResponse({'status': '-1', 'message': dict(user_form.errors.items())})
    return JsonResponse({'status': '-1', 'message': 'just POST request'})


@csrf_exempt
def register_organization(request):
    if request.method == "POST":
        print(request.POST)
        user_form = OrgUserSignupForm(request.POST)
        user_profile_form = UserProfileSignupForm(request.POST)
        org_form = OrgSignUpForm(request.POST)
        if user_form.is_valid():
            if user_profile_form.is_valid():
                if org_form.is_valid():
                    user = user_form.save()
                    user_profile = user_profile_form.save(commit=False)
                    user_profile.user = user
                    user_profile.save()
                    benefactor_form = org_form.save(commit=False)
                    benefactor_form.profile = user_profile
                    benefactor_form.save()
                    return JsonResponse({'status': '0'})
                else:
                    return JsonResponse({'status': '-1', 'message': dict(org_form.errors.items())})
            else:
                return JsonResponse({'status': '-1', 'message': dict(user_profile_form.errors.items())})
        else:
            return JsonResponse({'status': '-1', 'message': dict(user_form.errors.items())})
    return JsonResponse({'status': '-1', 'message': 'just POST request'})


@csrf_exempt
def all_login(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return JsonResponse({'status': '0', 'message': 'Successful Login'})

            return JsonResponse({'status': '-1', 'message': 'User is not active'})

        return JsonResponse({'status': '-1', 'message': 'User not found'})

    return JsonResponse({'status': '-1', 'message': 'just POST request'})
