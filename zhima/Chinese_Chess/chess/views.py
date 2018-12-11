from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from AllModular.database_operation import *
from AllModular.home_operation import *
import json
# Create your views here.


def homeurl(request):
    """
    登录页面
    :param request:
    :return: 返回首页html
    """
    return render(request, 'login.html')


def sta_auth(request):
    """
    登录请求函数
    :param request:
    :return:
    """
    if request.method == "POST":
        acc = request.POST.get('usr')
        pas = request.POST.get('psw')
        # 此处调用数据库中的个人信息表, 判断用户名username是否存在, 存在则返回
        kwa = login(account=acc, password=pas)
        if 'false' in kwa:
            return HttpResponse("账号不存在")
        else:
            if pas == kwa['password']:
                # 此处为密码正确
                print('密码正确')
                return HttpResponse(json.dumps("Ok"))
            else:
                return HttpResponse("密码错误")


def log_home(request):
    """
    到游戏主页
    :param request:
    :return:
    """
    return HttpResponse(json.dumps('OK'))


def home(request):
    """
    验证后成功登录到首页
    :param request:
    :return:
    """
    return render(request, 'home.html')


def log_auth(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        acc = request.POST.get('nickN')
        n_id = request.POST.get('ID')
    return HttpResponse(json.dumps("Ok"))
