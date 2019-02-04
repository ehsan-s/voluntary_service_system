from django.shortcuts import render
from .models import *
from apps.accounts.models import BenefactorProfile, OrganizationProfile, UserProfile
from django.http import JsonResponse
from django.db.models import F


#  http://127.0.0.1:8000/projects/organization/org/?type=non_financial&status=in_progress
def org_project(request, org_name):
    if request.method == 'GET':
        type = request.GET.get('type', 'financial')
        status = request.GET.get('status', 'done')
        projects_list = None
        if type == 'financial':
            projects_list = list(FinancialProject.objects\
                .filter(organization__profile__user__username=org_name, status=status)\
                .values('name', 'location', 'deadline', 'money_needed', 'money_donated'))
        elif type == 'non_financial':
            projects_list = list(NonFinancialProject.objects\
                .filter(organization__profile__user__username=org_name, status=status)\
                .annotate(category=F('need__category__category'), name=F('need__name'),
                        username=F('benefactor__profile__user__username'))\
                .values('category', 'name', 'username', 'location'))
        return JsonResponse({'status': '0', 'projects': projects_list})
    else:
        return JsonResponse({'status': '-1', 'error': 'this request method is not supported'})


def benefactor_project(request, benefactor_name):
    if request.method == 'GET':
        type = request.GET.get('type', 'financial')
        status = request.GET.get('status', 'done')
        print(benefactor_name, type, status)
        print(FinancialProject.objects.all()[0].benefactors.all())
        print(NonFinancialProject.objects.all().values())
        projects_list = None
        if type == 'financial':
            projects_list = list(FinancialProject.objects\
                .filter(benefactors__profile__user__username__exact=benefactor_name, status=status)\
                .annotate(username=F('organization__profile__user__username'))\
                .values('username', 'name', 'location', 'deadline', 'money_needed', 'money_donated'))
        elif type == 'non_financial':
            projects_list = list(NonFinancialProject.objects\
                .filter(benefactor__profile__user__username=benefactor_name, status=status)\
                .annotate(category=F('need__category__category'), name=F('need__name'),
                        username=F('organization__profile__user__username'))\
                .values('category', 'name', 'username', 'location'))
        return JsonResponse({'status': '0', 'projects': projects_list})
    else:
        return JsonResponse({'status': '-1', 'error': 'this request method is not supported'})


def org_feedback(request, org_name):
    if request.method == 'GET':
        type = request.GET.get('type', 'receive')
        feedbacks_list = None
        if type == 'receive':
            feedbacks_list = list(Feedback.objects\
                .filter(project__organization__profile__user__username=org_name, feeder='benefactor')
                                  .annotate(category=F('project__need__category__category'),
                                            name=F('project__need__name'),
                                            username=F('project__benefactor__profile__user__username'))
                                  .values('category', 'name', 'rate', 'feedback', 'username'))
        elif type == 'send':
            feedbacks_list = list(Feedback.objects\
                                  .filter(project__organization__profile__user__username=org_name, feeder='organization')
                                  .annotate(category=F('project__need__category__category'),
                                            name=F('project__need__name'),
                                            username=F('project__benefactor__profile__user__username'))
                                  .values('category', 'name', 'rate', 'feedback', 'username'))
        return JsonResponse({'status': '0', 'projects': feedbacks_list})
    else:
        return JsonResponse({'status': '-1', 'error': 'this request method is not supported'})


def benefactor_feedback(request, benefactor_name):
    if request.method == 'GET':
        type = request.GET.get('type', 'receive')
        feedbacks_list = None
        if type == 'receive':
            feedbacks_list = list(Feedback.objects\
                .filter(project__benefactor__profile__user__username=benefactor_name, feeder='organization')
                                  .annotate(category=F('project__need__category__category'),
                                            name=F('project__need__name'),
                                            username=F('project__organization__profile__user__username'))
                                  .values('category', 'name', 'rate', 'feedback', 'username'))
        elif type == 'send':
            feedbacks_list = list(Feedback.objects\
                                  .filter(project__benefactor__profile__user__username=benefactor_name, feeder='benefactor')
                                  .annotate(category=F('project__need__category__category'),
                                            name=F('project__need__name'),
                                            username=F('project__organization__profile__user__username'))
                                  .values('category', 'name', 'rate', 'feedback', 'username'))
        return JsonResponse({'status': '0', 'projects': feedbacks_list})
    else:
        return JsonResponse({'status': '-1', 'error': 'this request method is not supported'})
