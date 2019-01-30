from apscheduler.scheduler import Scheduler
import datetime
import hashlib


def time_curr():
    """
    获取当前时间
    :return: 返回字符串类型时间
    """
    string = datetime.datetime.now()
    time1_str = datetime.datetime.strftime(string, '%Y-%m-%d %H:%M:%S')
    return time1_str


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
