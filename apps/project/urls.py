from django.conf.urls import url
from apps.project import views

app_name = "project"
urlpatterns = [
    #url(r'^(?P<org>[0-9]+)/posts/$', views.posts, name='get_posts'),
    url(r'^organization/(?P<org_name>.+)/$', views.org_project, name='org_project'),
    #url(r'^login/$', views.LoginView.as_view(), name='login'),
]