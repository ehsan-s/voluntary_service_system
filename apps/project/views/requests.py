import json

from apps.project.models import *
from django.http import JsonResponse
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def org_request(request, org_name):
    if request.method == 'GET':
        type = request.GET.get('type', 'receive')
        requests_list = None
        requester = None
        if type == 'send':
            requester = 'organization'
        elif type == 'receive':
            requester = 'benefactor'
        if requester is not None:
            requests_list = list(Request.objects\
                .filter(project__organization__profile__user__username=org_name, requester=requester)
                                  .annotate(category=F('project__need__category__category'),
                                            name=F('project__need__name'), location=F('project__location'),
                                            username=F('benefactor__profile__user__username'))
                                  .values('username', 'category', 'name', 'location', 'request_desc', 'answer_desc', 'status'))
        return JsonResponse({'status': '0', 'requests': requests_list})
    else:
        return JsonResponse({'status': '-1', 'error': 'this request method is not supported'})


@csrf_exempt
def benefactor_request(request, benefactor_name):
    if request.method == 'GET':
        type = request.GET.get('type', 'receive')
        requests_list = None
        requester = None
        if type == 'receive':
            requester = 'organization'
        elif type == 'send':
            requester = 'benefactor'
        if requester is not None:
            requests_list = list(Request.objects\
                .filter(benefactor__profile__user__username=benefactor_name, requester=requester)
                                  .annotate(category=F('project__need__category__category'),
                                            name=F('project__need__name'), location=F('project__location'),
                                            username=F('project__organization__profile__user__username'))
                                  .values('username', 'category', 'name', 'location', 'request_desc', 'answer_desc', 'status'))
        return JsonResponse({'status': '0', 'requests': requests_list})
    else:
        return JsonResponse({'status': '-1', 'error': 'this request method is not supported'})


@csrf_exempt
def org_participation_request(request, benefactor_name, project_id):
    if request.method == 'POST':
        p = json.loads(request.body)
        description = p['request_desc']

        benefactor = BenefactorProfile.objects.get(profile__user__username=benefactor_name)
        project = NonFinancialProject.objects.get(id=project_id)

        if project.need in benefactor.skills:
            request = Request(benefactor=benefactor_name, project=project_id, requester='organization',
                              request_desc=description)
            request.save()
            return JsonResponse({'status': '0', 'message': 'request has been successfully submitted.'})

        else:
            return JsonResponse({'status': '-1', 'error': 'request is not valid.'})


@csrf_exempt
def benefactor_participation_request(request, benefactor_name, project_id):
    if request.method == 'POST':
        p = json.loads(request.body)
        description = p['request_desc']

        benefactor = BenefactorProfile.objects.get(profile__user__username=benefactor_name)
        project = NonFinancialProject.objects.get(id=project_id)

        if project.need in benefactor.skills:
            request = Request(benefactor=benefactor_name, project=project_id, requester='benefactor', request_desc=description)
            request.save()
            return JsonResponse({'status': '0', 'message': 'request has been successfully submitted.'})

        else:
            return JsonResponse({'status': '-1', 'error': 'request is not valid.'})
