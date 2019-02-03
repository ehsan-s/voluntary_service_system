from django.shortcuts import render
from .models import Project, FinancialProject, NonFinancialProject
from apps.accounts.models import BenefactorProfile, OrganizationProfile, UserProfile
from django.http import JsonResponse


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
            projects_list = NonFinancialProject.objects\
                .filter(organization__profile__user__username=org_name, status=status)\
                .values('need__category__category', 'need__name', '')
        return JsonResponse({'status': '0', 'projects': projects_list})
