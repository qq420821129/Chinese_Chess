from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
import re, time
import datetime


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=16,
                               min_length=6,
                               required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码',
                               max_length=16,
                               min_length=6,
                               required=False,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):
        username = self.cleaned_data.get('username', "")
        password = self.cleaned_data.get('password', "")
        if self.user.is_authenticated:
            auth.logout(self.request)
            raise forms.ValidationError('用户已登录')
        user = auth.authenticate(username=username, password=password)

        if user is None or not User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名或密码不正确')
        self.cleaned_data['user'] = user
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if not User.objects.filter(username=username).exists():
    #         raise forms.ValidationError('用户名不存在')
    #     return username

    # def clean_password(self):
    #     password = self.cleaned_data['password']
    #     if password in ['111111']:
    #         raise forms.ValidationError('密码太过简单')
    #     return password


class RegForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=16,
        min_length=6,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_name', 'placeholder': '请输入6-16位用户名'}))
    password = forms.CharField(
        label='密码',
        max_length=16,
        min_length=6,
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入6-16位密码'}))
    password_again = forms.CharField(
        label='二次密码',
        max_length=16,
        min_length=6,
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '再输入一次密码'}))
    email = forms.EmailField(
        label='邮箱',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入要绑定的邮箱', "id": "email_code"}))
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '邮箱查看验证码', "id": "input_code"}
        )
    )
    rname = forms.CharField(
        label='真实名字',
        min_length=2,
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入真实名字'}))
    idcard = forms.CharField(
        label='身份证',
        max_length=18,
        min_length=18,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入身份证号'}))
    tele = forms.CharField(
        label='手机号',
        max_length=11,
        min_length=11,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入手机号'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        if len(username) < 6:
            raise forms.ValidationError('用户名不能少于6位')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已绑定其他账号')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password in ['111111']:
            raise forms.ValidationError('密码过与简单')
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

    def clean_verification_code(self):
        verification_code(self)


    def clean_idcard(self):
        idcard = self.cleaned_data['idcard']
        r = re.compile(r'\d{17}(?:\d|X|x)?')
        if r.findall(idcard):
            b = idcard[6:10]
            year = datetime.datetime.now().year  # 获取当前年份
            if 1900 < int(b) <= year:
                return idcard
        raise forms.ValidationError('身份证错误')


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        required=False,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入绑定过的邮箱', "id": "email_code"}
        )
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '邮箱查看验证码', "id": "input_code"}
        )
    )
    new_password = forms.CharField(
        label="新的密码",
        max_length=16,
        min_length=6,
        required=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': "请输入新密码"}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email').strip()
        if not email:
            raise forms.ValidationError('邮箱不能为空')
        return email

    def clean_verification_code(self):
        verification_code(self)

    def clean_new_password(self):
        new_password(self)


def verification_code(self):
    verification_code = self.cleaned_data.get('verification_code').strip()
    send_code_time = self.request.session.get('send_code_time', '')
    send_code = self.request.session.get('code', '')
    now = int(time.time())
    if verification_code == '':
        raise forms.ValidationError('验证码不能为空')
    print('--------', send_code, verification_code)
    if send_code_time == '' or send_code == '':
        raise forms.ValidationError('你还没有获取验证码')
    if not (send_code.upper() == verification_code.upper()):
        raise forms.ValidationError('验证码不正确')
    if now - send_code_time > 1800:
        raise forms.ValidationError('验证码过期, 请重新获取')
    else:
        del self.request.session['send_code_time']
        del self.request.session['code']
    return verification_code


def new_password(self):
    email = self.cleaned_data.get('email')
    email = User.objects.filter(email=email).first()
    new_password = self.cleaned_data.get('new_password').strip()
    if new_password in ['111111', '']:
        raise forms.ValidationError('密码过于简单')
    email.set_password(new_password)
    email.save()
    return new_password
