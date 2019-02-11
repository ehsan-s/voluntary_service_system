from django.conf.urls import url
from apps.admin import views
from apps.accounts import views as vu

app_name = "accounts"
urlpatterns = [
    url(r'^view/benefactors/$', views.view_all_benefactors, name='view_all_benefactors'),
    url(r'^view/organizations/$', views.view_all_organizations, name='view_all_organizations'),
    url(r'^view/fprojects/$', views.view_all_fprojects, name='view_all_financial_projects'),
    url(r'^view/fprojects_ben/(?P<user_name>.+)/$', views.view_benefactor_fprojects, name='view_benefactor_financial_projects'),
    url(r'^view/fprojects_org/(?P<user_name>.+)/$', views.view_organization_fprojects, name='view_organization_financial_projects'),
url(r'^view/fprojects/$', views.view_all_nprojects, name='view_all_non-financial_projects'),
    url(r'^view/fprojects_ben/(?P<user_name>.+)/$', views.view_benefactor_nprojects, name='view_benefactor_non-financial_projects'),
    url(r'^view/fprojects_org/(?P<user_name>.+)/$', views.view_organization_nprojects, name='view_organization_non-financial_projects'),
    url(r'^view/skills/$', views.view_skills, name='view_all_skills'),
    url(r'^view/feedback_ben/$', views.view_benefactor_feedback, name='view_benfactor_feedback_for_organization'),
    url(r'^view/feedback_org/$', views.view_organization_feedback, name='view_organization_feedback_for_benfactor'),

    url(r'^manage/skills/$', views.add_skill, name='add_new_skill'),
    url(r'^manage/users/verify/(?P<user_name>.+)/$', views.verify_user, name='user_authentication'),
    url(r'^manage/users/remove/(?P<user_name>.+)/$', views.remove_user, name='user_removal'),
    url(r'^manage/feedback/edit/(?P<feedback_id>.+)/$', views.edit, name='feedback_authentication'),
    url(r'^manage/feedback/remove/(?P<feedback_id>.+)/$', views.remove_feedback, name='feedback_removal'),

    url(r'^benefactor/signup/$', vu.register_benefactor, name='benefactor_signup'),
    url(r'^organization/signup/$', vu.register_organization, name='org_signup'),
    url(r'^login/$', vu.login, name='login')
]
