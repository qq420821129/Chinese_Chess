"""ZhimaChess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
import os
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.views.static import serve
from . import views


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    url(r'^images/(?P<path>.*)$', serve, {'document_root': BASE_DIR + '/static/images'}),
    url(r'^js/(?P<path>.*)$', serve, {'document_root': BASE_DIR + '/static/js'}),
    url(r'^css/(?P<path>.*)$', serve, {'document_root': BASE_DIR  + '/static/css'}),
    url(r"^test$",views.hello,name="test")
]
