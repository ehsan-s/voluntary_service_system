import json
from apps.admin.models import Log
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
        return JsonResponse({'status': '-1', 'message': 'this request method is not supported'})


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
                                  .values('username', 'category', 'name', 'location', 'request_desc', 'answer_desc',
                                          'status'))
        return JsonResponse({'status': '0', 'requests': requests_list})
    else:
        return JsonResponse({'status': '-1', 'message': 'this request method is not supported'})


@csrf_exempt
def org_participation_request(request, benefactor_name, project_id):
    if request.method == 'POST':
        p = json.loads(request.body)
        description = p['request_desc']

        benefactor = BenefactorProfile.objects.get(profile__user__username=benefactor_name)
        project = NonFinancialProject.objects.get(id=project_id)

        if project.need in benefactor.skills:
            project_schedule = project.schedule.all()
            benefactor_schedule = benefactor.schedule.all()
            flag = 0
            for schedule in project_schedule:
                if schedule not in benefactor_schedule:
                    flag = 1

            if flag == 1:
                return JsonResponse({'status': '-1', 'message': 'Schedule does not match.'})

            else:
                request = Request(benefactor=benefactor_name, project=project_id, requester='organization',
                                  request_desc=description)
                request.save()
                organization = project.organization.profile.user.username
                Log(message='send request from organization {} to benefactor {} for project {}'.format(organization,
                                                                                                       benefactor_name,
                                                                                                       project_id)).save()
                return JsonResponse({'status': '0', 'message': 'request has been successfully submitted.'})
        else:
            return JsonResponse({'status': '-1', 'message': 'Benefactor does not fit the need.'})
    else:
        return JsonResponse({'status': '-1', 'message': 'request is not valid.'})


@csrf_exempt
def benefactor_participation_request(request, benefactor_name, project_id):
    if request.method == 'POST':
        p = json.loads(request.body)
        description = p['request_desc']

        benefactor = BenefactorProfile.objects.get(profile__user__username=benefactor_name)
        project = NonFinancialProject.objects.get(id=project_id)

        if project.need in benefactor.skills:
            project_schedule = project.schedule.all()
            benefactor_schedule = benefactor.schedule.all()
            flag = 0
            for schedule in project_schedule:
                if schedule not in benefactor_schedule:
                    flag = 1

            if flag == 1:
                return JsonResponse({'status': '-1', 'message': 'Schedule does not match.'})

            else:
                request = Request(benefactor=benefactor_name, project=project_id, requester='benefactor',
                                  request_desc=description)
                request.save()
                organization = project.organization.profile.user.username
                Log(message='send request from benefactor {} to organization {} for project {}'.format(benefactor_name,
                                                                                                       organization,
                                                                                                       project_id)).save()
                return JsonResponse({'status': '0', 'message': 'Request has been successfully submitted.'})
        else:
            return JsonResponse({'status': '-1', 'message': 'Benefactor does not fit the need.'})
    else:
        return JsonResponse({'status': '-1', 'message': 'request is not valid.'})


@csrf_exempt
def benefactor_pay(request, benefactor_name, project_id):
    if request.method == 'POST':
        p = json.loads(request.body)

        benefactor = BenefactorProfile.objects.get(profile__user__username=benefactor_name)
        if BenefactorProfile.DoesNotExist:
            return JsonResponse({'status': '-1', 'message': 'benefactor does not exist'})

        project = FinancialProject.objects.get(id=project_id)
        if FinancialProject.DoesNotExist:
            return JsonResponse({'status': '-1', 'message': 'financial project does not exist'})

        donation = p['amount']
        project.money_donated += donation
        if benefactor not in project.benefactors:
            project.benefactors.add(benefactor)
        organization = project.organization.profile.user.username
        Log(message='{} paid by benefactor {} for project with id {} of organization {}'.format(str(donation),
                                                                                                benefactor_name,
                                                                                                project_id,
                                                                                                organization)).save()
        return JsonResponse({'status': '0', 'message': 'payment has been successfully accomplished.'})

    else:
        return JsonResponse({'status': '-1', 'message': 'request is not valid.'})


@csrf_exempt
def project_accept(request, benefactor_name, project_id):
    if request.method == 'POST':
        benefactor = BenefactorProfile.objects.get(profile__user__username=benefactor_name)
        project = NonFinancialProject.objects.get(id=project_id)

        if project.benefactor is None:
            project.benefactor = benefactor
            project.save()
            benefactor.nonfinancialproject_set.add(project)
            benefactor.save()
            request = Request.objects.get(benefactor__profile__user__username=benefactor_name, project__id=project_id)
            if Request.DoesNotExist:
                return JsonResponse({'status': '-1', 'message': 'request does not exist'})
            else:
                request.status = 'accepted'
                request.save()
                organization = request.project.organization.profile.user.username
                if request.requester == 'benefactor':
                    Log(message='request by benefactor {} for project with id {} of organization'
                                ' {} is accepted'.format(benefactor_name, project_id, organization)).save()
                else:
                    Log(message='request by organization {} of project with id {} to benefactor'
                                ' {} is accepted'.format(organization, project_id, benefactor_name)).save()
                return JsonResponse({'status': '0', 'message': 'benefactor accepted the request.'})
        else:
            return JsonResponse({'status': '-1', 'message': 'request was successfully accepted'})
    else:
        return JsonResponse({'status': '-1', 'message': 'request is not valid.'})


@csrf_exempt
def project_reject(request, benefactor_name, project_id):
    if request.method == 'POST':
        request = Request.objects.get(benefactor__profile__user__username=benefactor_name, project__id=project_id)
        if Request.DoesNotExist:
            return JsonResponse({'status': '-1', 'message': 'request does not exist'})
        else:
            request.status = 'rejected'
            request.save()
            organization = request.project.organization.profile.user.username
            if request.requester == 'benefactor':
                Log(message='request by benefactor {} for project with id {} of organization'
                            ' {} is rejected'.format(benefactor_name, project_id, organization)).save()
            else:
                Log(message='request by organization {} of project with id {} to benefactor'
                            ' {} is rejected'.format(organization, project_id, benefactor_name)).save()
            return JsonResponse({'status': '0', 'message': 'request was successfully rejected.'})
    else:
        return JsonResponse({'status': '-1', 'message': 'request is not valid.'})


@csrf_exempt
def view_schedule_benefactor(request, benefactor_name):
    if request.method == "GET":
        benefactor = BenefactorProfile.objects.get(profile__user__username=benefactor_name)
        if BenefactorProfile.DoesNotExist:
            return JsonResponse({'status': '-1', 'error': 'benefactor does not exist.'})

        return JsonResponse({'status': '0', 'list': benefactor.get_schedule_list()})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def add_schedule_benefactor(request, benefactor_name):
    if request.method == 'POST':
        p = json.loads(request.body)
        schedule_times = p['schedule_times']

        benefactor = BenefactorProfile.objects.get(profile__user__username=benefactor_name)
        if BenefactorProfile.DoesNotExist:
            return JsonResponse({'status': '-1', 'error': 'benefactor does not exist.'})

        benefactor.schedule.clear()
        schedule_times = json.loads(schedule_times)
        for entry in schedule_times:
            schedule = Schedule(day=entry['day'], time=entry['time'])
            benefactor.schedule.add(schedule)
        benefactor.save()
        return JsonResponse({'status': '0', 'message': 'schedule added successfully.'})

    else:
        return JsonResponse({'status': '-1', 'error': 'request is not valid.'})


@csrf_exempt
def view_schedule_project(request, project_id):
    if request.method == "GET":
        project = NonFinancialProject.objects.get(id=project_id)
        if NonFinancialProject.DoesNotExist:
            return JsonResponse({'status': '-1', 'error': 'project does not exist.'})

        return JsonResponse({'status': '0', 'list': project.get_schedule_list()})

    else:
        return JsonResponse({'status': '-1', 'message': {'category': ['Request is invalid']}})


@csrf_exempt
def add_schedule_project(request, project_id):
    if request.method == 'POST':
        p = json.loads(request.body)
        schedule_times = p['schedule_times']

        project = NonFinancialProject.objects.get(id=project_id)
        if NonFinancialProject.DoesNotExist:
            return JsonResponse({'status': '-1', 'error': 'project does not exist.'})

        project.schedule.clear()
        schedule_times = json.loads(schedule_times)
        for entry in schedule_times:
            schedule = Schedule(day=entry['day'], time=entry['time'])
            project.schedule.add(schedule)
        project.save()
        return JsonResponse({'status': '0', 'message': 'schedule added successfully.'})

    else:
        return JsonResponse({'status': '-1', 'error': 'request is not valid.'})


@csrf_exempt
def end_project(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(id=project_id)
        if Project.DoesNotExist:
            return JsonResponse({'status': '-1', 'message': 'project does not exist'})
        else:
            project.status = 'done'
            project.save()
            benefactor_name = project.benefactor.profile.user.username
            organization = project.organization.profile.user.username
            Log(message='project with id {} of organization is done benefactor {}'.format(benefactor_name, project_id,
                                                                                          organization)).save()
            return JsonResponse({'status': '0', 'message': 'project is done.'})
    else:
        return JsonResponse({'status': '-1', 'message': 'request is not valid.'})
