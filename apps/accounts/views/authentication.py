from django.views.decorators.csrf import csrf_exempt
from apps.accounts.forms import (BenefactorSignUpForm, UserProfileSignupForm, BenefactorUserSignupForm,
                                 OrgUserSignupForm, OrgSignUpForm)
from apps.accounts.models import UserProfile
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from apps.accounts.models import SkillCategory, BenefactorSkill, BenefactorProfile, AdminProfile
from django.http import JsonResponse
from apps.admin.models import Log
import json
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from apps.accounts.tokens import account_activation_token
from django.contrib.auth.models import User


@csrf_exempt
def register_benefactor(request):
    if request.method == "POST":
        p = json.loads(request.body)
        user_form = BenefactorUserSignupForm(p)
        user_profile_form = UserProfileSignupForm(p)
        benefactor_form = BenefactorSignUpForm(p)

        skills = p['skills']
        skills = json.loads(skills)
        benefactor_skills = []
        for skill in skills:
            try:
                category = skill['category']
            except KeyError:
                return JsonResponse({'status': '-1', 'message': {'category': ['category is required']}})
            try:
                name = skill['name']
            except KeyError:
                return JsonResponse({'status': '-1', 'message': {'name': ['name is required']}})
            try:
                skill_category = SkillCategory.objects.get(category=category)
            except SkillCategory.DoesNotExist:
                skill_category = SkillCategory(category=category)
                skill_category.save()
            try:
                benefactor_skill = BenefactorSkill.objects.get(name=name)
            except BenefactorSkill.DoesNotExist:
                benefactor_skill = BenefactorSkill(name=name)
                benefactor_skill.category = skill_category
                benefactor_skill.save()
            benefactor_skills.append(benefactor_skill)
        if user_form.is_valid():
            if user_profile_form.is_valid():
                if benefactor_form.is_valid():
                    user = user_form.save()
                    user_profile = user_profile_form.save(commit=False)
                    user_profile.user = user
                    user_profile.generate_token()
                    user_profile.save()
                    benefactor = benefactor_form.save(commit=False)
                    benefactor.profile = user_profile
                    benefactor.save()
                    for skill in benefactor_skills:
                        benefactor.skills.add(skill)
                    log = Log(message='Benefactor {} registered'.format(user.username))
                    log.save()
                    return JsonResponse({'status': '0', 'message': 'Benefactor registered successfully'})
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
        p = json.loads(request.body)
        user_form = OrgUserSignupForm(p)
        user_profile_form = UserProfileSignupForm(p)
        org_form = OrgSignUpForm(p)
        if user_form.is_valid():
            if user_profile_form.is_valid():
                if org_form.is_valid():
                    user = user_form.save()
                    user_profile = user_profile_form.save(commit=False)
                    user_profile.user = user
                    user_profile.generate_token()
                    user_profile.save()
                    org = org_form.save(commit=False)
                    org.profile = user_profile
                    org.save()
                    log = Log(message='Organization {} registered'.format(user.username))
                    log.save()
                    return JsonResponse({'status': '0', 'message': 'Organization registered successfully'})
                else:
                    return JsonResponse({'status': '-1', 'message': dict(org_form.errors.items())})
            else:
                return JsonResponse({'status': '-1', 'message': dict(user_profile_form.errors.items())})
        else:
            return JsonResponse({'status': '-1', 'message': dict(user_form.errors.items())})
    return JsonResponse({'status': '-1', 'message': 'just POST request'})


@csrf_exempt
def login(request):
    if request.method == "POST":
        p = json.loads(request.body)
        login_form = AuthenticationForm(data=p)
        if login_form.is_valid():
            user = login_form.get_user()
            try:
                AdminProfile.objects.get(user__username=user.username)
                auth_login(request, user)
                Log(message='Admin {} get login'.format(user.username)).save()
                return JsonResponse({'status': '0', 'message': 'Successful Login', 'user': 'admin'})
            except AdminProfile.DoesNotExist:
                user_profile = UserProfile.objects.get(user__username=user.username)
                user_profile.generate_token()
                if user_profile.status != 'C':
                    return JsonResponse({'status': '-1', 'message': 'User not activated'})

                auth_login(request, user)
                if BenefactorProfile.objects.filter(profile__user__username=user.username).exists():
                    log = Log(message='Benefactor {} get login'.format(user.username))
                    log.save()
                    return JsonResponse({'status': '0', 'token': user_profile.token, 'message': 'Successful Login', 'user': 'benefactor'})
                else:
                    log = Log(message='Organization {} get login'.format(user.username))
                    log.save()
                    return JsonResponse({'status': '0', 'token': user_profile.token, 'message': 'Successful Login', 'user': 'organization'})
        else:
            return JsonResponse({'status': '-1', 'message': dict(login_form.errors.items())})
    else:
        return JsonResponse({'status': '-1', 'message': 'just POST request'})


@csrf_exempt
def logout(request):
    if request.method == "POST":
        p = json.loads(request.body)
        auth_logout(request)
        try:
            username = p['username']
        except KeyError:
            return JsonResponse({'status': '0', 'message': [{'username': 'This field is required'}]})

        if BenefactorProfile.objects.filter(profile__user__username=username).exists():
            Log(message='Benefactor {} get logout'.format(username)).save()
            return JsonResponse({'status': '0', 'message': 'Successful Login', 'user': 'benefactor'})
        else:
            Log(message='Organization {} get logout'.format(username)).save()
            return JsonResponse({'status': '0', 'message': 'Successful Logout', 'user': 'organization'})
    else:
        return JsonResponse({'status': '-1', 'message': 'not POST request'})

@csrf_exempt
def activate(request, uidb64, token):
    if request.method == "GET":
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.user_profile.status = 'C'
            user.save()
            user.user_profile.save()
            return JsonResponse({'status': '0', 'message': 'User activated.'})
        else:
            return JsonResponse({'status': '-1', 'message': 'wrong token'})
    else:
        return JsonResponse({'status': '-1', 'message': 'just POST request'})
