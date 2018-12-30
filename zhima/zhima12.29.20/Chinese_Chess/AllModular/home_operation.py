import hashlib


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


