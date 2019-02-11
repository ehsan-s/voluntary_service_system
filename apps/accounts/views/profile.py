from django.views.decorators.csrf import csrf_exempt
from apps.accounts.models import *
from apps.accounts.models import BenefactorProfile, OrganizationProfile, UserProfile
from django.http import JsonResponse


@csrf_exempt
def org_views_org(request, username):
    if request.method == "GET":
        org_profile = OrganizationProfile.objects.get(profile__user__username=username)
        return JsonResponse({'status': '0', 'data': org_profile.as_json()})
    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def benefactor_views_benefactor(request, username):
    if request.method == "GET":
        benefactor_profile = BenefactorProfile.objects.get(profile__user__username=username)
        return JsonResponse({'status': '0', 'data': benefactor_profile.as_json()})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def benefactor_views_org(request, username):
    if request.method == "GET":
        org_profile = OrganizationProfile.objects.get(profile__user__username=username)
        return JsonResponse({'status': '0', 'data': org_profile.as_json()})
    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def org_views_benefactor(request, username):
    if request.method == "GET":
        benefactor_profile = BenefactorProfile.objects.get(profile__user__username=username)
        return JsonResponse({'status': '0', 'data': benefactor_profile.as_json()})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})
