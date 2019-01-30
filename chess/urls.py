from django.urls import path
import os
from .views import *
from django.conf.urls import url
from django.views.static import serve

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    # 普通get url
    # path('', log, name='log'),
    path('', login, name='login'),  # 登录界面
    path('register', register, name='register'),  # 注册界面
    path('match_other', match_other, name='match_other'),  # 匹配
    path('match', match, name='match'),  # 再次开始游戏
    path('loginout', loginout, name='loginout'),
    path('out', out, name='out'),
    path('ready_start', ready_start, name='ready_start'),
    path('start', start, name='start'),
    path('echo', echo),
    path('play', play, name='play'),
    path('chess/info', info, name='info'),
    path('forpass', forpass, name='forpass'),
    path('send_verification_code/', send_verification_code, name='code'),
    path('send_code/', send_verification_code, name='send_code'),
    # path('homepage', homepage, name='homepage'),
    # path('valide_name', valide_name, name='valide_name')
]

urlpatterns += [
    # 页面渲染url
    url(r'^images/(?P<path>.*)$', serve, {'document_root': BASE_DIR + '/static/images'}),
    url(r'^js/(?P<path>.*)$', serve, {'document_root': BASE_DIR + '/static/js'}),
    url(r'^css/(?P<path>.*)$', serve, {'document_root': BASE_DIR + '/static/css'}),
]
