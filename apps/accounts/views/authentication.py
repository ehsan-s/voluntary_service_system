from django.views.decorators.csrf import csrf_exempt
from apps.accounts.forms import (BenefactorSignUpForm, UserProfileSignupForm, BenefactorUserSignupForm,
                                 OrgUserSignupForm, OrgSignUpForm)
from apps.accounts.models import UserProfile
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from apps.accounts.models import SkillCategory, BenefactorSkill, BenefactorProfile
from django.http import JsonResponse
from apps.admin.models import Log
import json


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

            user_profile = UserProfile.objects.get(user__username=user.username)
            if user_profile.status == 'P':
                return JsonResponse({'status': '-1', 'message': 'User not verified'})

            auth_login(request, user)
            if BenefactorProfile.objects.filter(profile__user__username=user.username).exists():
                log = Log(message='Benefactor {} has a login'.format(user.username))
                log.save()
                return JsonResponse({'status': '0', 'message': 'Successful Login', 'user': 'benefactor'})
            else:
                log = Log(message='Organization {} has a login'.format(user.username))
                log.save()
                return JsonResponse({'status': '0', 'message': 'Successful Login', 'user': 'organization'})
        else:
            return JsonResponse({'status': '-1', 'message': dict(login_form.errors.items())})
    else:
        return JsonResponse({'status': '-1', 'message': 'just POST request'})
