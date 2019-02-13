from django.views.decorators.csrf import csrf_exempt
from apps.search.forms import organizationNonFinancialForm, benefactorNonFinancialForm
from apps.accounts.models import (User, UserProfile, BenefactorProfile, OrganizationProfile,
                                  SkillCategory, BenefactorSkill)
from apps.project.models import NonFinancialProject, FinancialProject
from django.http import JsonResponse
import json


@csrf_exempt
def organization_search(request):
    if request.method == "POST":
        p = json.loads(request.body)
        if p['gender'] is None or p['gender'] == '':
            p['gender'] = 'اهمیتی ندارد'
        org_search_form = organizationNonFinancialForm(p)
        if org_search_form.is_valid():
            benefactors = BenefactorProfile.objects.all()
            if org_search_form.cleaned_data['city'] is not None and org_search_form.cleaned_data['city'] != '':
                benefactors = benefactors.filter(profile__city=org_search_form.cleaned_data['city'])
            if org_search_form.cleaned_data['gender'] is not 'اهمیتی ندارد' and org_search_form.cleaned_data['gender'] != '':
                benefactors = benefactors.filter(gender=org_search_form.cleaned_data['gender'])
            if org_search_form.cleaned_data['benefactor_username'] is not None and org_search_form.cleaned_data['benefactor_username'] != '':
                benefactors = benefactors.filter(profile__user__username=org_search_form.cleaned_data['benefactor_username'])
            skills = p['skills']
            if skills is not None and len(skills) != 0:
                benefactors = filter_benefactors_by_skill(benefactors, skills)
            data = []
            for ben in benefactors:
                data.append(ben.as_json())
            return JsonResponse({'status': '0', 'search': data})
        else:
            return JsonResponse({'status': '-1', 'message': dict(org_search_form.errors.items())})
    else:
        return JsonResponse({'status': '-1', 'error': 'this request method is not supported'})


@csrf_exempt
def benefactor_nonfinancial_search(request):
    if request.method == "POST":
        p = json.loads(request.body)
        print(p)
        if p['gender'] is None or p['gender'] == '':
            p['gender'] = 'اهمیتی ندارد'
        benefactor_search_form = benefactorNonFinancialForm(p)
        print(benefactor_search_form.errors)
        if benefactor_search_form.is_valid():
            projects = NonFinancialProject.objects.filter(status='not_started')
            for project in NonFinancialProject.objects.all():
                print(project.status)
            if benefactor_search_form.cleaned_data['city'] is not None and benefactor_search_form.cleaned_data['city'] != '':
                projects = projects.filter(location=benefactor_search_form.cleaned_data['city'])
            if benefactor_search_form.cleaned_data['gender'] != 'اهمیتی ندارد' and benefactor_search_form.cleaned_data['gender'] != '':
                projects = projects.filter(gender=benefactor_search_form.cleaned_data['gender'])
            if benefactor_search_form.cleaned_data['org_username'] is not None and benefactor_search_form.cleaned_data['org_username'] != '':
                projects = projects.filter(organization__profile__user__username=benefactor_search_form.cleaned_data['org_username'])
            if benefactor_search_form.cleaned_data['project_name'] is not None and benefactor_search_form.cleaned_data['project_name'] != '':
                projects = projects.filter(name=benefactor_search_form.cleaned_data['project_name'])
            skills = p['skills']
            if skills is not None and len(skills) != 0:
                projects = filter_projects_by_skill(projects, skills)

            data = []
            for project in projects:
                data.append(project.as_json())
            print(data)
            return JsonResponse({'status': '0', 'search': data})
        else:
            return JsonResponse({'status': '-1', 'message': dict(benefactor_search_form.errors.items())})
    else:
        return JsonResponse({'status': '-1', 'error': 'this request method is not supported'})


@csrf_exempt
def benefactor_financial_search(request):
    if request.method == "GET":
        data = []
        print(FinancialProject.objects.all())
        for project in FinancialProject.objects.filter(status='in_progress'):
            data.append(project.as_json())
        return JsonResponse({'status': '0', 'search': data})
    else:
        return JsonResponse({'status': '-1', 'error': 'this request method is not supported'})


def filter_benefactors_by_skill(benefactors, skills):
    res = []
    for ben in benefactors:
        contains = False
        for ben_skill in ben.get_all_skills():
            for skill in skills:
                if ben_skill == skill:
                    contains = True
        if contains:
            res.append(ben)
    return res


def filter_projects_by_skill(projects, skills):
    res = []
    for proj in projects:
        contains = False
        for skill in skills:
            if skill == proj.need.as_json():
                contains = True
        if contains:
            res.append(proj)
    return res