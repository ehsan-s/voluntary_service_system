from django.conf.urls import url
from apps.accounts import views

app_name = "accounts"
urlpatterns = [
    url(r'^benefactor/signup/$', views.register_benefactor, name='benefactor_signup'),
    url(r'^organization/signup/$', views.register_organization, name='org_signup'),
    url(r'^login/$', views.login, name='login'),

    url(r'^organization/profile/(?P<username>.+)/$', views.org_views_org, name='view_org_profile'),
    url(r'^benefactor/profile/(?P<username>.+)/$', views.benefactor_views_benefactor, name='view_benefactor_profile'),
    url(r'^organization/public_profile/(?P<username>.+)/$', views.benefactor_views_org, name='view_org_profile'),
    url(r'^benefactor/public_profile/(?P<username>.+)/$', views.org_views_benefactor, name='view_benefactor_profile'),

    url(r'^organization/edit_profile/(?P<username>.+)/$', views.edit_org, name='edit_org_profile'),
    url(r'^benefactor/edit_profile/(?P<username>.+)/$', views.edit_benefactor, name='edit_benefactor_profile'),
    url(r'^change_password/(?P<username>.+)/$', views.edit_password, name='edit_password')
]
