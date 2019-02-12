from apps.project.models import *
from apps.project.forms import FinancialProjectForm, NonFinancialProjectForm
from apps.accounts.models import OrganizationProfile
from apps.admin.models import Log
from django.http import JsonResponse
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def add_financial_project(request, org_name):
    if request.method == 'POST':
        p = json.loads(request.body)
        organization_profile = OrganizationProfile.objects.get(profile__user__username=org_name)
        financial_project_form = FinancialProjectForm(p)
        if financial_project_form.is_valid():
            financial_project = financial_project_form.save(commit=False)
            financial_project.organization = organization_profile
            financial_project.save()
            Log(message='Financial project with id {} added by {}'.format(financial_project.id, org_name)).save()
            return JsonResponse({'status': '0', 'message': 'Financial project added successfully'})
        else:
            return JsonResponse({'status': '-1', 'message': dict(financial_project_form.errors.items())})
    else:
        return JsonResponse({'status': '-1', 'message': 'just POST request'})


@csrf_exempt
def add_non_financial_project(request, org_name):
    if request.method == "POST":
        p = json.loads(request.body)
        organization_profile = OrganizationProfile.objects.get(profile__user__username=org_name)
        non_financial_project_form = NonFinancialProjectForm(p)
        skill = p['need']
        skill = json.loads(skill)
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
        if non_financial_project_form.is_valid():
            non_financial_project = non_financial_project_form.save(commit=False)
            non_financial_project.organization = organization_profile
            non_financial_project.need = benefactor_skill
            non_financial_project.save()
            Log(message='Non-financial project with id {} added by {}'.format(non_financial_project.id, org_name)).save()
            return JsonResponse({'status': '0', 'message': 'Non-Financial project added successfully'})
        else:
            return JsonResponse({'status': '-1', 'message': dict(non_financial_project_form.errors.items())})
    else:
        return JsonResponse({'status': '-1', 'message': 'just POST request'})

#  http://127.0.0.1:8000/projects/organization/org/?type=non_financial&status=in_progress
@csrf_exempt
def org_project(request, org_name):
    if request.method == 'GET':
        type = request.GET.get('type', 'financial')
        status = request.GET.get('status', 'done')
        projects_list = None
        if type == 'financial':
            projects_list = list(FinancialProject.objects\
                .filter(organization__profile__user__username=org_name, status=status)\
                .values('name', 'deadline', 'money_needed', 'money_donated'))
        elif type == 'non_financial':
            projects_list = list(NonFinancialProject.objects\
                .filter(organization__profile__user__username=org_name, status=status)\
                .annotate(category=F('need__category__category'), skill_name=F('need__name'),
                          project_name=F('name'), username=F('benefactor__profile__user__username'))\
                .values('category', 'skill_name', 'username', 'project_name', 'location', 'id'))
        return JsonResponse({'status': '0', 'projects': projects_list})
    else:
        return JsonResponse({'status': '-1', 'error': 'this request method is not supported'})


@csrf_exempt
def benefactor_project(request, benefactor_name):
    if request.method == 'GET':
        type = request.GET.get('type', 'financial')
        status = request.GET.get('status', 'done')
        # print(benefactor_name, type, status)
        # print(FinancialProject.objects.all()[0].benefactors.all())
        # print(NonFinancialProject.objects.all().values())
        projects_list = None
        if type == 'financial':
            projects_list = list(FinancialProject.objects\
                .filter(benefactors__profile__user__username__exact=benefactor_name, status=status)\
                .annotate(username=F('organization__profile__user__username'))\
                .values('username', 'name', 'deadline', 'money_needed', 'money_donated'))
        elif type == 'non_financial':
            projects_list = list(NonFinancialProject.objects\
                .filter(benefactor__profile__user__username=benefactor_name, status=status)\
                .annotate(category=F('need__category__category'), skill_name=F('need__name'),
                          project_name=F('name'), username=F('organization__profile__user__username'))\
                .values('category', 'skill_name', 'username', 'project_name', 'location', 'id'))
        return JsonResponse({'status': '0', 'projects': projects_list})
    else:
        return JsonResponse({'status': '-1', 'error': 'this request method is not supported'})
