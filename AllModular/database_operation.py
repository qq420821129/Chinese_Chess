from django.shortcuts import render
from ..chess.models import *
from django.utils import timezone

# Create your views here.
"""这是对mysql数据库所有表的增删改查的模块文件"""
DeBug = True


def Log(*str):
    if DeBug:
        print(str)


def getUser(account):
    users = UserInfo.objects.filter(account=account)
    return users.first()


def login(**kwargs):
    """
    登录数据库操作
    :param kwargs: 账号account
    :return: 存在返回密码password/昵称nickname, 否则返回false
    """
    account = kwargs['account']
    user = getUser(account)
    if user:
        dict = {}
        dict['password'] = user.password
        dict['nickname'] = user.nickname
        user.last_login_time = timezone.localtime()
        try:
            user.save()
            return dict
        except Exception as e:
            print('database error %s' % e)
            return False
    else:
        return False


def register(**kwargs):
    """
    注册数据库操作
    :param kwargs: 账号account/密码password/昵称nickname
                   姓名c_name/身份证号c_IDcard/电话c_tele
    :return: 全部执行成功返回true, 否则返回false
    """
    account = kwargs['account']
    user = getUser(account)
    if user:
        return False
    user = UserInfo()
    for k, v in kwargs.items():
        setattr(user, k, v)
    if 'nickname' not in kwargs:
        user.nickname = account
    try:
        user.save()
        return True
    except Exception as e:
        print('database error', e)
        return False


def finish_game(**kwargs):
    """
    对战完成一局游戏
    更新战绩表                          result
    :param kwargs: 账号account/胜victory/平draw/负defeat/积分变化score
    :return: 全部执行成功返回true, 否则返回false
    """
    account = kwargs['account']
    user = getUser(account)
    if user:
        vic = Victory.objects.filter(user=user).first()

        if vic:
            vic.total += 1
        else:
            vic = Victory()
            for k, v in kwargs.items():
                setattr(vic, k, v)
            vic.total = 1
            vic.user = user

        result = kwargs['result']
        index = result.index(1)
        victory = draw = defeat = 0

        if index == 0:
            victory = 1
        elif index == 1:
            draw = 1
        else:
            defeat = 1
        vic.victory = victory
        vic.draw = draw
        vic.defeat = defeat

        try:
            vic.save()
            return True
        except Exception as e:
            print("database error", e)
            return False


def add_friends(**kwargs):
    """
    添加好友
    :param kwargs: account/个人IDf_sid/好友IDf_oid
    :return: 全部执行成功返回true, 否则返回false
    """
    account = kwargs['account']
    user = getUser(account)
    f = Friend()
    f.f_sid = user.pk
    f.f_oid = kwargs['f_oid']
    f.content_object = user
    try:
        f.save()
        return True
    except Exception as e:
        print("database error")
        return False


def ch_cookie(account, cookie):
    """
    更改cookie值
    :param cookie:
    :param account:
    :return:
    """
    user = getUser(account)
    user.token = cookie
    try:
        user.save()
    except Exception as e:
        print("database error", e)
        return False
    return True


