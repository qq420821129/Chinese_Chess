from django.urls import path
import os
from .views import *
from django.conf.urls import url
from django.views.static import serve

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    # 普通get url
    path('', login, name='login'),  # 登录界面
    path('register', register, name='register'),  # 注册界面
    # path('match', match, name='match')  # 匹配
]


# urlpatterns += [
#     # 页面渲染url
#     url(r'^images/(?P<path>.*)$', serve, {'document_root': BASE_DIR + '/static/images'}),
#     url(r'^js/(?P<path>.*)$', serve, {'document_root': BASE_DIR + '/static/js'}),
#     url(r'^css/(?P<path>.*)$', serve, {'document_root': BASE_DIR + '/static/css'}),
# ]
