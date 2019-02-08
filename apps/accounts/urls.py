from django.conf.urls import url
from apps.accounts import views

app_name = "accounts"
urlpatterns = [
    url(r'^benefactor/signup/$', views.register_benefactor, name='benefactor_signup'),
    url(r'^organization/signup/$', views.register_organization, name='org_signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^organization/profile/(?P<username>.+)/$', views.edit_org, name='org_profile'),
    url(r'^benefactor/profile/(?P<username>.+)/$', views.edit_benefactor, name='benefactor_profile'),
    url(r'^change_password/(?P<username>.+)/$', views.edit_password, name='edit_password'),
]
