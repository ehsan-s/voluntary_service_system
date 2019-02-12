from django.conf.urls import url
from apps.search import views

app_name = "search"
urlpatterns = [
    url(r'^organization/$', views.organization_search, name='organization_search'),
    url(r'^benefactor/non_financial/$', views.benefactor_nonfinancial_search, name='benefactor_nonfinancial_search'),
    url(r'^benefactor/financial/$', views.benefactor_financial_search, name='benefactor_financial_search'),
]