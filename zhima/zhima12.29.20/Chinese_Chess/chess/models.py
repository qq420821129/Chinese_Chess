from django.db import models
import django.utils.timezone as timezone
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


# Create your models here.
# 个人信息
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=16)  # 昵称
    rname = models.CharField(max_length=16)  # 名字
    idcard = models.CharField(max_length=18)  # 身份证
    tele = models.CharField(max_length=11)  # 手机号
    friends = GenericRelation('Friend')
    
    def __str__(self):
        return "%s" % self.idcard


# 好友
class Friend(models.Model):
    f_sid = models.IntegerField()  # 自我id
    f_oid = models.IntegerField()  # 对方id

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return "%s-%s" % (self.f_sid, self.f_oid)


# 战绩
class Victory(models.Model):
    total = models.IntegerField(default=0)  # 总计
    victory = models.IntegerField(default=0)  # 胜场
    draw = models.IntegerField(default=0)  # 平场
    defeat = models.IntegerField(default=0)  # 负场
    score = models.IntegerField(default=1000)  # 积分

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s-%s-%s-%s-%s" % (self.total, self.victory, self.draw, self.defeat, self.score)


# 房间
class Room(models.Model):
    # rnum = models.IntegerField()  # 房间号
    red = models.ForeignKey(User, related_name='house_user1', on_delete=models.CASCADE)  # 红方
    blue = models.ForeignKey(User, related_name='house_user2', on_delete=models.CASCADE, default='')  # 蓝方
    state = models.CharField(max_length=16, choices=(('0', 'empty'), ('1', 'wait'), ('2', 'full')), default='wait')  # 状态

    def __str__(self):
        return "%s-%s-%s" % (self.red, self.blue, self.state)
