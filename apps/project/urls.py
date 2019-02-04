from django.conf.urls import url
from apps.project import views

app_name = "project"
urlpatterns = [
    url(r'^organization/(?P<org_name>.+)/$', views.org_project, name='org_project'),
    url(r'^benefactor/(?P<benefactor_name>.+)/$', views.benefactor_project, name='benefactor_project'),
    url(r'^feedbacks/organization/(?P<org_name>.+)/$', views.org_feedback, name='org_feedback'),
    url(r'^feedbacks/benefactor/(?P<benefactor_name>.+)/$', views.benefactor_feedback, name='benefactor_feedback'),
]