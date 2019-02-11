import json
from apps.project.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def add_skill(request):
    if request.method == 'POST':
        p = json.loads(request.body)
        category = p['category']
        name = p['name']

        existing_skill_category = SkillCategory.objects.get(category=category)
        if existing_skill_category is None:
            skill_category = SkillCategory(category=category)
            skill_category.save()
            benefactor_skill = BenefactorSkill(name=name, category=skill_category)
            benefactor_skill.save()
            return JsonResponse({'status': '0', 'message': 'skill has been successfully added.'})

        elif BenefactorSkill.objects.get(name=name, category__category=category) is None:
            benefactor_skill = BenefactorSkill(name=name, category=existing_skill_category)
            benefactor_skill.save()

        else:
            return JsonResponse({'status': '-1', 'error': 'duplicate skill'})

    else:
        return JsonResponse({'status': '-1', 'error': 'request is not valid.'})


@csrf_exempt
def verify_user(request, user_name):
    if request.method == 'POST':
        try:
            user = UserProfile.objects.get(user__username=user_name)
        except UserProfile.DoesNotExist:
            return JsonResponse({'status': '-1', 'error': 'user does not exist.'})

        user.status = 'V'
        user.save()
        return JsonResponse({'status': '0', 'message': 'user has been successfully verified.'})

    else:
        return JsonResponse({'status': '-1', 'error': 'request is not valid.'})


@csrf_exempt
def remove_user(request, user_name):
    if request.method == 'POST':
        try:
            user = UserProfile.objects.get(user__username=user_name)
        except UserProfile.DoesNotExist:
            return JsonResponse({'status': '-1', 'error': 'user does not exist.'})

        user.delete()
        return JsonResponse({'status': '0', 'message': 'user has been successfully removed.'})

    else:
        return JsonResponse({'status': '-1', 'error': 'request is not valid.'})


@csrf_exempt
def edit_feedback(request, feedback_id):
    pass


@csrf_exempt
def remove_feedback(request, feedback_id):
    if request.method == 'POST':
        try:
            feedback = Feedback.objects.get(id=feedback_id)
        except Feedback.DoesNotExist:
            return JsonResponse({'status': '-1', 'error': 'feedback does not exist.'})

        feedback.delete()
        return JsonResponse({'status': '0', 'message': 'feedback has been successfully removed.'})

    else:
        return JsonResponse({'status': '-1', 'error': 'request is not valid.'})
