from django.shortcuts import render, redirect
from .forms import LoginForm, RegForm, ForgotPasswordForm
from django.http import HttpResponse, JsonResponse
from dwebsocket.decorators import accept_websocket
from AllModular.game_fiction import *
import random, string, time
from django.core.mail import send_mail
from django.db.models import Q


def stati_out():
    print('启动项目')
    room_state = Room.objects.filter(~Q(state='empty')).all()
    for i in room_state:
        i.red = None
        i.blue = None
        i.state = 'empty'
        i.save()


stati_out()


def Debug(e=None, static=True):
    if static:
        print(e)


def forpass(request):
    """找回密码"""
    if request.method == "POST":
        forpass = ForgotPasswordForm(request.POST, request=request)
        email = request.POST.get('email')
        if email:
            if forpass.is_valid():
                return redirect("/")
    else:
        forpass = ForgotPasswordForm()
    data = {'forpass': forpass}
    return render(request, 'forpass.html', data)


def send_verification_code(request):
    """邮箱认证"""
    data = {}
    if request.method == 'GET':
        email = request.GET.get('email')
        name_mail = request.GET.get('type')
        email_user = User.objects.filter(email=email).first()
        if email_user or name_mail == '注册':
            if email:
                # 生成验证码
                code1 = ''.join(random.sample(string.ascii_letters + string.digits, 4))
                now = int(time.time())
                send_code_time = request.session.get('send_code_time', 0)
                if now - send_code_time < 30:
                    data['status'] = 'ERROR1'
                else:
                    request.session['send_code_time'] = now
                    request.session['code'] = code1
                    # 发送邮件
                    try:
                        send_mail(
                            name_mail,
                            '[智码象棋]验证码：%s \n(有效期30分钟)\n您收到这封电子邮件是因为您 (也可能是某人冒充您的名义) 在智码象'
                            '棋中%s。假如这不是您本人的操作, 您可不予理会 (但勿泄露他人)。' % (code1, name_mail),
                            '1562047185@qq.com',
                            [email],
                            fail_silently=False
                        )
                        data['status'] = 'SUCCESS'
                        print(code1)
                        print('发送成功')
                    except Exception as e:
                        data['status'] = 'ERROR1'
                        print('邮件发送异常', e)
        else:
            data["status"] = 'ERROR2'
        return JsonResponse(data)


def echo(request):
    """注册账号实时验证"""
    user_in = request.POST.get('user')
    user = User.objects.filter(username=user_in).first()
    if user:
        return HttpResponse(json.dumps({'data': True}))
    return HttpResponse(json.dumps({'data': False}))


@accept_websocket
def info(request):
    """连接websocket长连接"""
    if request.is_websocket():
        user = request.user
        # 得到对手用户名
        room = Room.objects.filter(red=user).first()
        if room:
            Debug('玩家[%s]房间号[%s]对手是黑方' % (user, room.rnum))
            user_lin = room.blue
        else:
            room = Room.objects.filter(blue=user).first()
            Debug('玩家[%s]房间号[%s]对手是黑方' % (user, room.rnum))
            user_lin = room.red

        Current_Board(str(room.rnum))
        global allconn
        # 将用户名与websocket存入全局字典
        allconn[str(user)] = request.websocket
        websocket_log(request, user, room, user_lin)


def login(request):
    """首页登录"""
    if request.method == 'POST':
        login_form = LoginForm(request.POST, user=request.user, request=request)
        if login_form.is_valid():
            # 登录用户
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            victory = user.victory
            # 进入房间
            side, other, first, room_rnum = app_room(user)
            Debug('玩家[%s], 进入匹配页面, 正在查找可匹配玩家...' % user)
            return render(request, 'match.html', context={'victory': victory, 'side': side, 'other': other, 'first': first, 'room': room_rnum})
    else:
        login_form = LoginForm()

    context = {'login_form': login_form}
    return render(request, 'login.html', context)


def match(request):

    if request.method == 'GET' and request.user.userinfo.state != 'outline':
        user = request.user
        Debug('游戏结束, 玩家[%s], 进入匹配页面, 正在查找可匹配玩家...' % user)
        victory = user.victory
        # 进入房间
        side, other, first, room_rnum = app_room(user)
        return render(request, 'match.html',
                      context={'victory': victory, 'side': side, 'other': other, 'first': first, 'room': room_rnum})


def out(request):
    Debug('收到退出请求')
    if request.method == "POST":
        user = request.user
        Debug('发送退出响应')
        out_room(user)
        user.userinfo.state = 'outline'
        user.userinfo.save()
        auth.logout(request)
        print(user, "退出登录状态")
        return HttpResponse(json.dumps({'data': 'true'}))


def register(request):
    """注册"""
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
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
            return redirect("/")
    else:
        reg_form = RegForm()

    context = {'register_form': reg_form}
    return render(request, 'register.html', context)


def match_other(request):
    """匹配"""
    user = request.user
    uroom = request.GET.get('room')
    if request.method == 'GET':
        room = Room.objects.filter(rnum=uroom).first()
        if room.state == 'full':
            Debug('找到可匹配玩家')
            user.userinfo.state = 'waitready'
            user.userinfo.save()
            if room.red == user:
                other = room.blue
            else:
                other = room.red
            result = 'OK'
        else:
            other = None
            result = 'NO'
        if other:
            other = {'username': other.username, 'victory': other.victory.victory, 'defeat': other.victory.defeat, 'draw': other.victory.draw,
                     'score': other.victory.score}
        context = {'result': result, 'other': other}
        return HttpResponse(json.dumps(context))


def loginout(request):
    """前端发起退出"""
    user = request.user
    user.userinfo.state = 'outline'
    user.userinfo.save()
    print(user, "退出登录状态")
    print(user.userinfo.state)
    auth.logout(request)
    return redirect('/')


class utime:
    """读秒类"""
    t_room = {}

    def __init__(self, uroom):
        self.utime = 0
        self.uroom = uroom
        utime.t_room[uroom] = self

    def changeTime(self, side):
        if side == 'red':
            self.utime += 1
        else:
            self.utime -= 1
        if abs(self.utime) == 10:
            return True


def ready_start(request):
    """开始游戏轮询读秒"""
    user = request.user
    uroom = request.POST.get('room')
    side = request.POST.get('side')
    if uroom in utime.t_room:
        u = utime.t_room.get(uroom)
    else:
        u = utime(uroom)
    room = Room.objects.filter(rnum=uroom).first()
    re = u.changeTime(side)
    other = 'unready'
    if room.state != 'full':
        other = 'exit'
        user.userinfo.state = 'wait'
        user.userinfo.save()
    if re:
        del utime.t_room[uroom]
        print('删除房间定时计次 :', utime.t_room)
        return HttpResponse(json.dumps({'times': 60}))
    else:
        return HttpResponse(json.dumps({'other': other}))


def start(request):
    """进入游戏判断"""
    print('---------------', 'start')
    uroom = request.POST.get('room')
    user = request.user
    if not user.is_authenticated:
        return
    print('222/--设置玩家状态: ready')
    user.userinfo.state = 'ready'
    user.userinfo.save()

    room = Room.objects.filter(rnum=uroom).first()
    other = room.red if room.blue == user else room.blue
    if not other or other.userinfo.state == 'outline':
        print('333/--设置玩家状态: wait')
        user.userinfo.state = 'wait'
        user.userinfo.save()
        info = {'other': 'exit'}
    elif other.userinfo.state in ['ready', 'playing']:
        info = {'result': 'OK'}
    else:
        info = ''
    return HttpResponse(json.dumps(info))


def play(request):
    """成功匹配"""
    print('post参数', request.POST)
    uroom = request.POST.get('room')
    user = request.user
    if not user.is_authenticated:
        return
    print('444/--设置玩家状态为: playing')
    user.userinfo.state = 'playing'
    user.userinfo.save()

    print('uroom---->', uroom)
    room = Room.objects.filter(rnum=uroom).first()
    if room.red == user:
        side = 1
    else:
        side = -1

    victory = user.victory
    if room.red == user:
        other = room.blue
    else:
        other = room.red
    return render(request, 'chess.html', context={'victory': victory, 'user': user, 'side': side, 'other': other, 'room': uroom})
