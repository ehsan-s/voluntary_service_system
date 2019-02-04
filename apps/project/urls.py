from django.conf.urls import url
from apps.project import views

app_name = "project"
urlpatterns = [
    url(r'^organization/(?P<org_name>.+)/$', views.org_project, name='org_project'),
    url(r'^benefactor/(?P<benefactor_name>.+)/$', views.benefactor_project, name='benefactor_project'),
    #url(r'^(?P<org>[0-9]+)/posts/$', views.posts, name='get_posts'),
    #url(r'^login/$', views.LoginView.as_view(), name='login'),
]