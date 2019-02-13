import json
from apps.project.models import *
from apps.admin.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def view_all_benefactors(request):
    if request.method == "GET":
        data = []
        try:
            for benefactor in BenefactorProfile.objects.all():
                data.append(benefactor.as_json())
            return JsonResponse({'status': '0', 'list': data})
        except BenefactorProfile.DoesNotExist:
            return JsonResponse({'status': '0', 'list': data})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def view_pending_benefactors(request):
    if request.method == "GET":
        data = []
        for benefactor in BenefactorProfile.objects.all():
            if benefactor.profile.status == 'P':
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
def view_pending_organizations(request):
    if request.method == "GET":
        data = []
        for organization in OrganizationProfile.objects.all():
            if organization.profile.status == 'P':
                data.append(organization.as_json())
        return JsonResponse({'status': '0', 'list': data})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def view_all_fprojects(request):
    if request.method == "GET":
        data = []
        for project in FinancialProject.objects.all():
            data.append(project.as_json())
        return JsonResponse({'status': '0', 'list': data})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def view_benefactor_fprojects(request, username):
    if request.method == "GET":
        benefactor = BenefactorProfile.objects.get(profile__user__username=username)
        data = []
        for project in FinancialProject.objects.all():
            if benefactor in project.benefactors.all():
                data.append(project.as_json())
        return JsonResponse({'status': '0', 'list': data})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def view_organization_fprojects(request, username):
    if request.method == "GET":
        orgnanization = OrganizationProfile.objects.get(profile__user__username=username)
        data = []
        for project in FinancialProject.objects.all():
            if orgnanization.id == project.organization.id:
                data.append(project.as_json())
        return JsonResponse({'status': '0', 'list': data})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})

@csrf_exempt
def view_all_nprojects(request):
    if request.method == "GET":
        data = []
        for project in NonFinancialProject.objects.all():
            data.append(project.as_json())
        return JsonResponse({'status': '0', 'list': data})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def view_benefactor_nprojects(request, username):
    if request.method == "GET":
        benefactor = BenefactorProfile.objects.get(profile__user__username=username)
        data = []
        for project in NonFinancialProject.objects.all():
            if benefactor.id == project.benefactor.id:
                data.append(project.as_json())
        return JsonResponse({'status': '0', 'list': data})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def view_organization_nprojects(request, username):
    if request.method == "GET":
        orgnanization = OrganizationProfile.objects.get(profile__user__username=username)
        data = []
        for project in NonFinancialProject.objects.all():
            if orgnanization.id == project.organization.id:
                data.append(project.as_json())
        return JsonResponse({'status': '0', 'list': data})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def view_skills(request):
    if request.method == "GET":
        data = []
        try:
            for skill in BenefactorSkill.objects.all():
                data.append(skill.as_json())
            return JsonResponse({'status': '0', 'list': data})
        except BenefactorSkill.DoesNotExist:
            return JsonResponse({'status': '0', 'list': data})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def view_benefactor_feedback(request):
    if request.method == "GET":
        data = []
        try:
            for feedback in Feedback.objects.get(feeder='benefactor'):
                data.append(feedback.as_json())
            return JsonResponse({'status': '0', 'list': data})
        except Feedback.DoesNotExist:
            return JsonResponse({'status': '0', 'list': data})
    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def view_organization_feedback(request):
    if request.method == "GET":
        data = []
        try:
            for feedback in Feedback.objects.get(feeder='organization'):
                data.append(feedback.as_json())
            return JsonResponse({'status': '0', 'list': data})
        except Feedback.DoesNotExist:
            return JsonResponse({'status': '0', 'list': data})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def view_logs(request):
    if request.method == "GET":
        all_logs = list(Log.objects.all().values('message', 'time'))
        return JsonResponse({'status': '0', 'logs': all_logs})
    else:
        return JsonResponse({'status': '-1', 'logs': 'just POST request'})
