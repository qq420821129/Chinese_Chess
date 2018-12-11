from django.urls import path
import os
from .views import *
from django.conf.urls import url
from django.views.static import serve

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    # 普通get url
    path('', homeurl)  # 登录界面
]

urlpatterns += [
    # ajax静态url
    url(r'^static_auth$', sta_auth),  # 登录按钮ajax
    url(r'^login_home$', log_home),  # 验证成功
    url(r'login_auth', log_auth),  # 游客登录按钮
    url(r'^home', home),  # 验证后成功登录到首页
]

urlpatterns += [
    # 页面渲染url
    url(r'^images/(?P<path>.*)$', serve, {'document_root': BASE_DIR + '/static/images'}),
    url(r'^js/(?P<path>.*)$', serve, {'document_root': BASE_DIR + '/static/js'}),
    url(r'^css/(?P<path>.*)$', serve, {'document_root': BASE_DIR + '/static/css'}),
]
