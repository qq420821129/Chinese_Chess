"""这是对mysql数据库所有表的增删改查的模块文件"""


def login(**kwargs):
    """
    登录数据库操作
    :param kwargs: 登录时间time/账号account
    :return: 存在返回密码password/昵称nickname, 否则返回false
    """
    print(kwargs)
    kwa={'password': '3dd635a808ddb6dd4b6731f7c409d53dd4b14df2', 'nickname': '12345678'}
    return kwa


def register(**kwargs):
    """
    注册数据库操作
    :param kwargs: 登录时间time/账号account/密码password/昵称nickname
                   姓名c_name/身份证号c_IDcard/电话c_tele
    :return: 全部执行成功返回true, 否则返回false
    """
    pass


def finish_game(**kwargs):
    """
    对战完成一局游戏
    更新战绩表
    :param kwargs: 账号account/胜victory/平draw/负defeat
    :return: 全部执行成功返回true, 否则返回false
    """
    pass


def add_friends(**kwargs):
    """
    添加好友
    :param kwargs: 个人IDf_sid/好友IDf_oid
    :return: 全部执行成功返回true, 否则返回false
    """
    pass
