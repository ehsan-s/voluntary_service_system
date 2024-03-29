"""voluntary_service_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from apps.accounts import urls as account_urls
from apps.project import urls as project_urls
from apps.search import urls as search_urls
from apps.admin import urls as admin_urls

# from django.contrib import admin

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include(account_urls)),
    url(r'^projects/', include(project_urls)),
    url(r'^search/', include(search_urls)),
    url(r'^admin/', include(admin_urls))
]
