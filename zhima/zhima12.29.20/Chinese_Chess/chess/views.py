from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import LoginForm, RegForm
from .models import UserInfo
from django.http import HttpResponse, HttpResponseRedirect
import threading
import datetime
import json
import time
from .models import *

user_online = {}


def get_victory(username):
    user_name = User.objects.filter(username=username).first()
    victory = Victory.objects.filter(user=user_name).first()
    return victory


def login(request):
    """首页登录"""
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 登录用户
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            victory = get_victory(user)

            # 获取可匹配房间
            room_wait = Room.objects.filter(state='wait')
            if not room_wait:
                room_empty = Room.objects.filter(state='empty')
                if not room_empty:
                    # max_id = Room.objects.all().order_by("-id")[0]
                    user_name = User.objects.filter(username=user).first()
                    room = Room()
                    room.red = user_name
                    # room.blue = ''
                    room.save()
                    room_id = Room.objects.filter(red=user).id
                    print(room_id)
            # print(iiii)

            return render(request, 'match.html', context={'victory': victory})
    else:
        login_form = LoginForm()

    context = {'login_form': login_form}
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']
            rname = reg_form.cleaned_data['rname']
            idcard = reg_form.cleaned_data['idcard']
            tele = reg_form.cleaned_data['tele']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 保存用户
            userInfo = UserInfo()
            setattr(userInfo, 'rname', rname)
            setattr(userInfo, 'idcard', idcard)
            setattr(userInfo, 'tele', tele)
            user_name = User.objects.filter(username=username).first()
            userInfo.user = user_name
            userInfo.save()
            # 更新默认战绩值
            victory = Victory()
            victory.user = user_name
            victory.save()
            victory = Victory.objects.filter(user=user_name).first()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            # return redirect(request.GET.get('from', reverse('/')))
            return render(request, 'match.html', context={'victory': victory})
    else:
        reg_form = RegForm()

    context = {'register_form': reg_form}
    return render(request, 'register.html', context)

# .acquire()  获取信号量
# .release()  增加信号量

# def match(request):
#     try:
#         print(request.users)
#     except:
#         pass
#     print(request.user)
#     print(request.GET)
#     print(request.POST)
#     if request.method == 'POST':
#         pass
#     else:
#         return render(request, 'match.html')
