from django.views.decorators.csrf import csrf_exempt
from apps.accounts.forms import UserProfileEditForm, BenefactorProfileEditForm
from django.contrib.auth.forms import PasswordChangeForm
from apps.accounts.models import (User, UserProfile, BenefactorProfile, OrganizationProfile,
                                  SkillCategory, BenefactorSkill)
from django.http import JsonResponse
import json


@csrf_exempt
def edit_password(request, username):
    if request.method == "POST":
        user = User.objects.get(username=username)
        user_form = PasswordChangeForm(data=request.POST, user=user)
        if user_form.is_valid():
            user_form.save()
            return JsonResponse({'status': '0', 'message': 'Successful changing password'})
        else:
            return JsonResponse({'status': '-1', 'message': dict(user_form.errors.items())})
    else:
        return JsonResponse({'status': '-1'})


@csrf_exempt
def edit_org(request, username):
    if request.method == "POST":
        p = json.loads(request.body)
        user_profile = UserProfile.objects.get(user__username=username)
        user_profile_form = UserProfileEditForm(p, instance=user_profile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            return JsonResponse({'status': '0', 'message': 'Successful edit profile'})
        else:
            return JsonResponse({'status': '-1', 'message': dict(user_profile_form.errors.items())})
    else:
        org_profile = OrganizationProfile.objects.get(profile__user__username=username)
        return JsonResponse({'status': '0', 'data': org_profile.as_json()})


@csrf_exempt
def edit_benefactor(request, username):
    if request.method == "POST":
        p = json.loads(request.body)
        user_profile = UserProfile.objects.get(user__username=username)
        benefactor_profile = BenefactorProfile.objects.get(profile__user__username=username)
        user_profile_form = UserProfileEditForm(p, instance=user_profile)
        benefactor_profile_form = BenefactorProfileEditForm(p, instance=benefactor_profile)
        skills = p['skills']
        benefactor_skills = []
        for skill in skills:
            try:
                category = skill['category']
            except KeyError:
                return JsonResponse({'status': '-1', 'message': {'category': ['Category is required']}})
            try:
                name = skill['name']
            except KeyError:
                return JsonResponse({'status': '-1', 'message': {'Name': ['Name is required']}})
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
        if user_profile_form.is_valid():
            if benefactor_profile.is_valid():
                user_profile_form.save()
                benefactor_profile = benefactor_profile_form.save()
                benefactor_profile.skills.clear()
                for skill in benefactor_skills:
                    benefactor_profile.skills.add(skill)
                return JsonResponse({'status': '0', 'message': 'Successful edit profile'})
            else:
                return JsonResponse({'status': '-1', 'message': dict(benefactor_profile_form.errors.items())})
        else:
            return JsonResponse({'status': '-1', 'message': dict(user_profile_form.errors.items())})
    else:
        benefactor_profile = BenefactorProfile.objects.get(profile__user__username=username)
        benefactor_profile.get_all_skills()
        return JsonResponse({'status': '0', 'data': benefactor_profile.as_json()})
