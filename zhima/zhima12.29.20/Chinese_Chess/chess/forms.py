from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
import datetime


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=16,
                               min_length=6,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码',
                               max_length=16,
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):
        username = self.cleaned_data.get('username', "")
        password = self.cleaned_data.get('password', "")

        user = auth.authenticate(username=username, password=password)
        if user is None or not User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名或密码不正确')
        self.cleaned_data['user'] = user
        return self.cleaned_data

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
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入6-16位用户名'}))
    password = forms.CharField(
        label='密码',
        max_length=16,
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password_again = forms.CharField(
        label='二次密码',
        max_length=16,
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '再输入一次密码'}))
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}))
    rname = forms.CharField(
        label='真实名字',
        min_length=2,
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入真实名字'}))
    idcard = forms.CharField(
        label='身份证',
        max_length=18,
        min_length=18,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入身份证号'}))
    tele = forms.CharField(
        label='手机号',
        max_length=11,
        min_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入手机号'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password in ['111111']:
            raise forms.ValidationError('密码太过简单')
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

    def clean_idcard(self):
        idcard = self.cleaned_data['idcard']
        r = re.compile(r'\d{17}(?:\d|X|x$)')
        if r.findall(idcard):
            b = idcard[6:10]
            year = datetime.datetime.now().year  # 获取当前年份
            if 1900 < int(b) <= year:
                return idcard
        raise forms.ValidationError('身份证错误')


# class RegForm(forms.Form):
#     username = forms.CharField(label='用户名',
#                                max_length=16,
#                                min_length=4,
#                                widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入3-30位用户名'}))
#     email = forms.EmailField(label='邮箱',
#                              widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
#     password = forms.CharField(label='密码',
#                                max_length=16,
#                                min_length=6,
#                                widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
#     password_again = forms.CharField(label='再输入一次密码',
#                                      max_length=16,
#                                      min_length=6,
#                                      widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'再输入一次密码'}))
#
#     def clean_username(self):
#         username = self.cleaned_data['username']
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError('用户名已存在')
#         return username
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError('邮箱已存在')
#         return email
#
#     def clean_password_again(self):
#         password = self.cleaned_data['password']
#         password_again = self.cleaned_data['password_again']
#         if password != password_again:
#             raise forms.ValidationError('两次输入的密码不一致')
#         return password_again
#
# class ChangeNicknameForm(forms.Form):
#     nickname_new = forms.CharField(
#         label='新的昵称',
#         max_length=20,
#         widget=forms.TextInput(
#             attrs={'class':'form-control', 'placeholder': '请输入新的昵称'}
#         )
#     )
#
#     def __init__(self, *args, **kwargs):
#         if 'user' in kwargs:
#             self.user = kwargs.pop('user')
#         super(ChangeNicknameForm, self).__init__(*args, **kwargs)
#
#     def clean(self):
#         # 判断用户是否登录
#         if self.user.is_authenticated:
#             self.cleaned_data['user'] = self.user
#         else:
#             raise forms.ValidationError('用户尚未登录')
#         return self.cleaned_data
#
#     def clean_nickname_new(self):
#         nickname_new = self.cleaned_data.get('nickname_new', '').strip()
#         if nickname_new == '':
#             raise forms.ValidationError("新的昵称不能为空")
#         return nickname_new
#
# class BindEmailForm(forms.Form):
#     email = forms.EmailField(
#         label='邮箱',
#         widget=forms.EmailInput(
#             attrs={'class':'form-control', 'placeholder':'请输入正确的邮箱'}
#         )
#     )
#     verification_code = forms.CharField(
#         label='验证码',
#         required=False,
#         widget=forms.TextInput(
#             attrs={'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}
#         )
#     )
#
#     def __init__(self, *args, **kwargs):
#         if 'request' in kwargs:
#             self.request = kwargs.pop('request')
#         super(BindEmailForm, self).__init__(*args, **kwargs)
#
#     def clean(self):
#         # 判断用户是否登录
#         if self.request.user.is_authenticated:
#             self.cleaned_data['user'] = self.request.user
#         else:
#             raise forms.ValidationError('用户尚未登录')
#
#         # 判断用户是否已绑定邮箱
#         if self.request.user.email != '':
#             raise forms.ValidationError('你已经绑定邮箱')
#
#         # 判断验证码
#         code = self.request.session.get('bind_email_code', '')
#         verification_code = self.cleaned_data.get('verification_code', '')
#         if not (code != '' and code == verification_code):
#             raise forms.ValidationError('验证码不正确')
#
#         return self.cleaned_data
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError('该邮箱已经被绑定')
#         return email
#
#     def clean_verification_code(self):
#         verification_code = self.cleaned_data.get('verification_code', '').strip()
#         if verification_code == '':
#             raise forms.ValidationError('验证码不能为空')
#         return verification_code
