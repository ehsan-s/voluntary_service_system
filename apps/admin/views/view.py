import json
from apps.project.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def view_all_benefactors(request):
    if request.method == "GET":
        data = []
        for benefactor in BenefactorProfile.objects.all():
            data.append(benefactor.as_json())
        return JsonResponse({'status': '0', 'list': data})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def view_all_organizations(request):
    if request.method == "GET":
        data = []
        for organization in OrganizationProfile.objects.all():
            data.append(organization.as_json())
        return JsonResponse({'status': '0', 'list': data})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def view_skills(request):
    if request.method == "GET":
        data = []
        for skill in BenefactorSkill.objects.all():
            data.append(skill.as_json())
        return JsonResponse({'status': '0', 'list': data})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def view_benefactor_feedback(request):
    if request.method == "GET":
        data = []
        for feedback in Feedback.objects.get(feeder='benefactor', status='A'):
            data.append(feedback.as_json())
        return JsonResponse({'status': '0', 'list': data})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def view_organization_feedback(request):
    if request.method == "GET":
        data = []
        for feedback in Feedback.objects.get(feeder='organization', status='A'):
            data.append(feedback.as_json())
        return JsonResponse({'status': '0', 'list': data})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})
