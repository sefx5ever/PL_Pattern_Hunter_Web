"""Web_Pattern_Hunter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import path,include
from Login_System import views as login_view
from Dashboard_System import views as dashboard_view
from API import views as api_viewset


urlpatterns = [
    path('admin/',admin.site.urls),
    path('login/',login_view.login),
    path('register/',login_view.register),
    path('resetPassword/',login_view.reset_password),
    path('accountSetting/',dashboard_view.account_setting),
    path('dashboardUser/',dashboard_view.dashboard_user),
    path('api/', include('API.urls')),
    # path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
]


