from django.db import models

# Create your models here.

from django.db import models
import django.utils.timezone as timezone


# Create your models here.
class GRXX(models.Model):
    """个人信息表"""
    time = models.DateTimeField(auto_now_add=True)  # 登录时间
    account = models.CharField(max_length=16)  # 账号
    password = models.CharField(max_length=64)  # 密码
    nickname = models.CharField(max_length=16)  # 昵称


class HY(models.Model):
    """好友表"""
    f_sid = models.IntegerField()  # 个人ID
    f_oid = models.IntegerField()  # 好友ID
    f_id = models.ForeignKey(GRXX, on_delete=models.CASCADE)  # id


class PM(models.Model):
    """排名表"""
    r_ranking = models.IntegerField()  # id
    r_id = models.ForeignKey(GRXX, on_delete=models.CASCADE)  # 外键id


class ZJ(models.Model):
    """战绩表"""
    m_sum = models.IntegerField()  # 总局数
    m_victory = models.IntegerField()  # 胜局
    m_draw = models.IntegerField()  # 平局
    m_defeat = models.IntegerField()  # 负局
    m_id = models.ForeignKey(GRXX, on_delete=models.CASCADE)  # 外键id


class SMZ(models.Model):
    """实名制信息表"""
    c_name = models.CharField(max_length=16)  # 姓名
    c_IDcard = models.IntegerField()  # 身份证号
    c_tele = models.IntegerField(primary_key=True)  # 电话
    c_id = models.ForeignKey(GRXX, on_delete=models.CASCADE)  # 外键id
