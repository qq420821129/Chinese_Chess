import hashlib

"""
这是在网页首页操作的模块文件
包括登录/注册/游客功能
"""

def home(request):
    """
    首页
    :param request:
    :return:
    """
    if request.method == 'GET':
        # 首页url
        return render(request, 'home.html')

    elif request.method == 'POST':
        # 登录操作
        p_acc = request.POST.get('acc')
        p_pass = request.POST.get('pas')
        if not all([p_acc, p_pass]):
            # 存在空内容直接返回首页url
            return render(request, 'home.html')
        else:
            try:
                # 判断账号是否已存在
                acc_pass = user.objects.filter(account=p_acc)
            except Exception:
                # 不存在直接返回首页url
                return render(request, 'home.html')
            # 判断密码是否正确
            if acc_pass[2] != p_pass:
                # 密码错误
                return render(request, 'home.html')
            else:
                # 登录成功
                pass


def register(request):
    """
    注册页面
    :param request:
    :return:
    """
    if request.method == 'GET':
        # 切换注册url
        return render(request, 'register.html')

    elif request.method == 'POST':
        p_acc = request.POST.get('acc')
        p_pass1 = request.POST.get('pas1')
        p_pass2 = request.POST.get('pas2')
        p_name = request.POST.get('name')
        p_phone = request.POST.get('phone')
        p_IDcard = request.POST.get('IDcard')

        if not all([p_acc, p_pass1, p_pass2, p_name, p_IDcard]):
            # 存在空内容直接返回注册url
            return render(request, 'register.html')
        else:
            # 判断密码是否正确
            if p_pass1 != p_pass2 or len(p_pass1) != 40:
                # 两次密码不一致
                return render(request, 'register.html')
            try:
                # 判断账号是否已存在
                user.objects.filter(account=p_acc)
            except Exception:
                if 4 <= len(p_acc) <= 16:
                    pass
                else:
                    return render(request, 'register.html')
            else:
                return render(request, 'register.html')

            try:
                # 判断手机号是否已存在
                real_name.objects.filter(c_phone=p_phone)
            except Exception:
                pass
            else:
                return render(request, 'register.html')

            try:
                # 判断身份证是否已使用
                real_name.objects.filter(c_IDcard=p_IDcard)
            except Exception:
                judge = id_verification(p_IDcard)
                if not judge:
                    return render(request, 'register.html')
            else:
                return render(request, 'register.html')
            # 存入数据库
            pass


def tourist(request):
    """
    游客临时登录
    :return:
    """
    if request.method == 'GET':
        # 登陆成功后页面
        request.POST.get('nimane')
    elif request.method == 'POST':
        pass


def id_verification(p_IDcard):
    """
    身份证验证
    :param p_IDcard: 身份证号码
    :return: 正确返回True, 否则返回False
    """
    r = re.compile(r'\d{17}(?:\d|X|x$)')
    if r.findall(p_IDcard):
        b = p_IDcard[6:8]
        if b >= 19:
            return True
        else:
            return False
    else:
        return False


def str_sha1(st_r):
    """
    sha1加密函数
    :param st_r:
    :return:
    """
    print('调用了sha1加密')
    s = hashlib.sha1()
    s.update(st_r.encode('utf8'))
    pwd = s.hexdigest()  # 返回十六进制加密结果
    return pwd


# 登录：sha1 + 公私钥 --> 服务
# 注册：sha1 + 公私钥 --> 服务
