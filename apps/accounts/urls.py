from django.conf.urls import url
from apps.accounts import views

app_name = "accounts"
urlpatterns = [
    url(r'^signup-benefactor/', views.register_benefactor, name='benefactor_signup'),
    url(r'^signup-org/', views.register_organization, name='org_signup'),
    url(r'^login/$', views.all_login, name='login'),
]
