from apps.project.models import *
from apps.project.forms import FeedbackForm, NonFinancialProject
from django.http import JsonResponse
from django.db.models import F
from apps.admin.models import Log
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def send_feedback(request):
    if request.method == "POST":
        p = json.loads(request.body)
        print(p)
        feedback_form = FeedbackForm(p)
        non_financial_project = NonFinancialProject.objects.get(pk=p['id'])
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.project = non_financial_project
            feedback.save()
            print(feedback.feeder)
            org = feedback.project.organization.profile.user.username
            benefactor = feedback.project.benefactor.profile.user.username
            project_id = feedback.project.id
            if p['feeder'] == 'benefactor':
                Log(message='Feedback from {} to {} added for project {}'.format(benefactor, org, project_id)).save()
            else:
                Log(message='Feedback from {} to {} added for project {}'.format(org, benefactor, project_id)).save()
            return JsonResponse({'status': '0', 'message': 'feedback sent successfully'})
        else:
            return JsonResponse({'status': '-1', 'message': dict(feedback_form.errors.items())})
    else:
        return JsonResponse({'status': '-1', 'message': 'just POST request'})


@csrf_exempt
def org_feedback(request, org_name):
    if request.method == 'GET':
        type = request.GET.get('type', 'receive')
        feedbacks_list = None
        feeder = None
        if type == 'send':
            feeder = 'organization'
        elif type == 'receive':
            feeder = 'benefactor'
        if feeder is not None:
            feedbacks_list = list(Feedback.objects\
                .filter(project__organization__profile__user__username=org_name, feeder=feeder)
                                  .annotate(category=F('project__need__category__category'),
                                            skill_name=F('project__need__name'),
                                            username=F('project__benefactor__profile__user__username'),
                                            project_name=F('project__name'))
                                  .values('category', 'skill_name', 'rate', 'feedback', 'username', 'project_name'))
        return JsonResponse({'status': '0', 'feedbacks': feedbacks_list})
    else:
        return JsonResponse({'status': '-1', 'error': 'this request method is not supported'})


@csrf_exempt
def benefactor_feedback(request, benefactor_name):
    if request.method == 'GET':
        type = request.GET.get('type', 'receive')
        feedbacks_list = None
        feeder = None
        if type == 'receive':
            feeder = 'organization'
        elif type == 'send':
            feeder = 'benefactor'
        if feeder is not None:
            feedbacks_list = list(Feedback.objects\
                .filter(project__benefactor__profile__user__username=benefactor_name, feeder=feeder)
                                  .annotate(category=F('project__need__category__category'),
                                            skill_name=F('project__need__name'),
                                            username=F('project__organization__profile__user__username'),
                                            project_name=F('project__name'))
                                  .values('category', 'skill_name', 'rate', 'feedback', 'username', 'project_name'))
        return JsonResponse({'status': '0', 'feedbacks': feedbacks_list})
    else:
        return JsonResponse({'status': '-1', 'error': 'this request method is not supported'})
