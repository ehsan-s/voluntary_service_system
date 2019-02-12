from django.conf.urls import url
from apps.project import views

app_name = "project"
urlpatterns = [
    url(r'^organization/add_financial/(?P<org_name>.+)/$', views.add_financial_project, name='add_financial_project'),
    url(r'^organization/add_non_financial/(?P<org_name>.+)/$', views.add_non_financial_project, name='add_non_financial_project'),
    url(r'^organization/(?P<org_name>.+)/$', views.org_project, name='org_project'),
    url(r'^benefactor/(?P<benefactor_name>.+)/$', views.benefactor_project, name='benefactor_project'),
    url(r'^feedbacks/send/$', views.send_feedback, name='feedback'),
    url(r'^feedbacks/organization/(?P<org_name>.+)/$', views.org_feedback, name='org_feedback'),
    url(r'^feedbacks/benefactor/(?P<benefactor_name>.+)/$', views.benefactor_feedback, name='benefactor_feedback'),
    url(r'^requests/organization/(?P<org_name>.+)/$', views.org_request, name='org_request'),
    url(r'^requests/benefactor/(?P<benefactor_name>.+)/$', views.benefactor_request, name='benefactor_request'),
    url(r'^requests/organization/(?P<benefactor_name>.+)/(?P<project_id>.+)/$', views.org_participation_request, name='org_request'),
    url(r'^requests/benefactor/(?P<benefactor_name>.+)/(?P<project_id>.+)/$', views.benefactor_participation_request, name='benefactor_request'),
    url(r'^requests/benefactor/pay/(?P<benefactor_name>.+)/(?P<project_id>.+)/$', views.benefactor_pay, name='benefactor_pay_financial_project')
]
