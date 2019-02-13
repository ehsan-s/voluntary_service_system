from django.conf.urls import url
from apps.project import views

app_name = "project"
urlpatterns = [
    url(r'^organization/add_financial/(?P<org_name>.+)/$', views.add_financial_project, name='add_financial_project'),
    url(r'^organization/add_non_financial/(?P<org_name>.+)/$', views.add_non_financial_project, name='add_non_financial_project'),
    url(r'^organization/(?P<org_name>.+)/$', views.org_project, name='org_project'),


    url(r'^feedbacks/send/$', views.send_feedback, name='feedback'),
    url(r'^feedbacks/organization/(?P<org_name>.+)/$', views.org_feedback, name='org_feedback'),
    url(r'^feedbacks/benefactor/(?P<benefactor_name>.+)/$', views.benefactor_feedback, name='benefactor_feedback'),

    url(r'^requests/organization/(?P<benefactor_name>.+)/(?P<project_id>.+)/$', views.org_participation_request,name='org_request'),
    url(r'^requests/organization/(?P<org_name>.+)/$', views.org_request, name='org_request'),
    url(r'^requests/benefactor/pay/(?P<benefactor_name>.+)/(?P<project_id>.+)/$', views.benefactor_pay,name='benefactor_pay_financial_project'),
    url(r'^requests/benefactor/(?P<benefactor_name>.+)/(?P<project_id>.+)/$', views.benefactor_participation_request, name='benefactor_request'),
    url(r'^requests/benefactor/(?P<benefactor_name>.+)/$', views.benefactor_request, name='benefactor_request'),
    url(r'^requests/accept/(?P<benefactor_name>.+)/(?P<project_id>.+)/$', views.project_accept, name='accept_request'),
    url(r'^requests/reject/(?P<benefactor_name>.+)/(?P<project_id>.+)/$', views.project_reject, name='reject_request'),

    url(r'^benefactor/view_schedule/(?P<benefactor_name>.+)/$', views.view_schedule_benefactor, name='view_schedule_for_benefactor'),
    url(r'^benefactor/add_schedule/(?P<benefactor_name>.+)/$', views.add_schedule_benefactor, name='add_schedule_for_benefactor'),
    url(r'^benefactor/(?P<benefactor_name>.+)/$', views.benefactor_project, name='benefactor_project'),

    url(r'^project/view_schedule/(?P<project_id>.+)/$', views.view_schedule_project, name='view_schedule_for_project'),
    url(r'^project/add_schedule/(?P<project_id>.+)/$', views.add_schedule_project, name='add_schedule_for_project'),
    url(r'^project/done/(?P<project_id>.+)/$', views.end_project, name='end_project')
]

