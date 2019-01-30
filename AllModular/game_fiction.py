from chess.models import *
import json
from django.contrib import auth


class Current_Board:
    board = {}

    def __init__(self, room):
        """后端下棋许可验证对象"""
        self.c_b_position = [
                            [-3, -4, -5, -6, -7, -6, -5, -4, -3],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, -2, 0, 0, 0, 0, 0, -2, 0],
                            [-1, 0, -1, 0, -1, 0, -1, 0, -1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 0, 1, 0, 1, 0, 1, 0, 1],
                            [0, 2, 0, 0, 0, 0, 0, 2, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [3, 4, 5, 6, 7, 6, 5, 4, 3]
                            ]
        self.reco = []  # 存储悔棋步骤
        Current_Board.board[room] = self
        print('房间棋盘>', Current_Board.board)


def thismove(y, x, j, i, types, room):
    """下棋许可验证"""
    r = Current_Board.board.get(room)
    r.reco.append([y, x, j, i, types])
    if types < 0:
        # 转换棋子位置
        y, x = mation(y, x)
        j, i = mation(j, i)
    if types == r.c_b_position[y][x]:  # 判断当前位置棋子类型
        if r.c_b_position[j][i] != 0:
            r.reco[-1].append(r.c_b_position[j][i])
        r.c_b_position[y][x] = 0
        r.c_b_position[j][i] = types
        print('/////////////', r.c_b_position)
        return True
    else:
        print("[%s]号房间, 棋盘布局错误" % room)
        return False


def mation(y, x):
    """转换棋子位置"""
    y = 9 - y
    x = 8 - x
    return y, x


def uppermove(r):
    """ 悔棋操作"""
    print('可悔棋列表:', r.reco)
    upmove = r.reco.pop(-1)
    if upmove[4] < 0:
        # 转换棋子位置
        y, x = mation(upmove[0], upmove[1])
        j, i = mation(upmove[2], upmove[3])
    else:
        y, x = upmove[0], upmove[1]
        j, i = upmove[2], upmove[3]
    print('------------', y, x, j, i)
    if upmove[4] == r.c_b_position[j][i]:
        r.c_b_position[y][x] = upmove[4]
        if len(upmove) == 6:
            r.c_b_position[j][i] = upmove[5]
        else:
            r.c_b_position[j][i] = 0
        print(r.c_b_position)
        return [upmove[0], upmove[1]], [upmove[2], upmove[3]], upmove[4]
    else:
        print('悔棋棋盘错误')
        return False


allconn = {}


def one_user(past, now, types, request, send_type=1):
    """给自己回复消息"""
    if send_type:
        di = {'past': now, 'now': past, 'type': types}
    else:
        di = {'past': past, 'now': now, 'type': types}
    di = {'type': 'chess', 'dict': di}
    di = json.dumps(di).encode('utf-8')
    request.websocket.send(di)


def two_user(past, now, types, user_lin):
    """给对手回复消息"""
    di = {'past': past, 'now': now, 'type': types}
    di = {'type': 'chess', 'dict': di}
    di = json.dumps(di).encode('utf-8')
    print('di---构造为字典, 并JSON为字符串类型-->>', di)
    print(user_lin)
    allconn.get(str(user_lin)).send(di)


def app_room(user):
    """加入房间"""
    # 获取可匹配房间
    room = Room.objects.filter(state='wait')
    # print(room)
    if not room:
        # 没有匹配房间
        room = Room.objects.filter(state='empty')
        if not room:
            # 创建新房间
            room = Room()
        else:
            # 进入空房间
            room = room.first()
            room.state = 'wait'
            print('2.1/', str(user))
        room.red = user
        room.save()
        print('玩家[%s]进入了房间[%s]' % (str(user), room.rnum))
        side = 'red'
        other = ''
        first = 'true'
    else:
        # 进入有人匹配的房间
        room = room.first()
        if not room.red:
            room.red = user
            side = 'red'
            other = room.blue
        else:
            room.blue = user
            side = 'blue'
            other = room.red
        # else:
        #     user_sem = user_online[str(room.blue)]
        room.state = 'full'
        room.save()
        first = 'false'
    user.userinfo.state = 'wait'
    print('设置玩家状态成功')
    user.userinfo.save()
    print('房间号', room.rnum)
    return side, other, first, room.rnum


def out_room(user):
    """退出房间"""
    room = Room.objects.filter(red=user).first()
    if room:
        room.red = None
        if room.blue:
            room.state = 'wait'
        else:
            room.state = 'empty'
    else:
        room = Room.objects.filter(blue=user).first()
        if room:
            room.blue = None
            if room.red:
                room.state = 'wait'
            else:
                room.state = 'empty'
        else:
            room.state = 'empty'
    user.userinfo.state = 'wait'
    user.save()
    print('room', room, user, '退出')
    room.save()


def auth_logout(request, user):
    """退出登录"""
    out_room(user)
    user.userinfo.state = 'outline'
    user.userinfo.save()
    request.websocket.close()
    print(user, "退出登录状态")
    print(user.userinfo.state)
    auth.logout(request)


def mess_log(mess):
    """解析数据格式"""
    if mess:
        mess = mess.decode("utf-8")
        mess = json.loads(mess)
    return mess


def message_log(message, user, user_lin):
    """发送聊天消息"""
    content = message['content']
    print('收到消息: ', content)
    content = str(user) + ": " + content
    di = {"type": "talk", "dic": content}
    di = json.dumps(di).encode("utf-8")
    allconn.get(str(user_lin)).send(di)


def upvictory(user, banance, vtype, msg=''):
    """积分变更/提示信息拼接"""
    vdata = '+0+0+0'
    score = user.victory.score
    total = user.victory.total
    victory = user.victory.victory
    draw = user.victory.draw
    defeat = user.victory.defeat
    if banance:  # 投降结束游戏
        if not vtype:  # 失败
            user.victory.score -= 10
            msg += '你已经投降\n积分: %s <-- %s-10\n' % (user.victory.score, score)
    elif banance == 0:  # 通过将军结束游戏
        if not vtype:  # 失败
            user.victory.score -= 5
            msg += '你已经战败\n积分: %s <-- %s-5\n' % (user.victory.score, score)

    if not vtype:  # 失败
        user.victory.defeat += 1
        vdata = '+0+0+1'
    elif vtype == 1:  # 获胜
        user.victory.victory += 1
        user.victory.score += 10
        vdata = '+1+0+0'
        msg += '你已经获胜\n积分: %s <-- %s+10\n' % (user.victory.score, score)
    elif vtype == 2:  # 平局
        user.victory.draw += 1
        user.victory.score += 5
        vdata = '+0+1+0'
        msg += '你与对方势均力敌\n积分: %s <-- %s+5\n' % (user.victory.score, score)
    user.victory.total += 1
    user.victory.save()
    msg += '胜场: %s <-- %s%s\n' % (user.victory.victory, victory, vdata[0:2])
    msg += '平场: %s <-- %s%s\n' % (user.victory.draw, draw, vdata[2:4])
    msg += '负场: %s <-- %s%s\n' % (user.victory.defeat, defeat, vdata[4:6])
    msg += '总场: %s <-- %s+1' % (user.victory.total, total)
    return msg


def send_sub1(request, user, banance, vtype):
    msg = upvictory(user, banance, vtype)
    request.websocket.send(json.dumps({"type": 'banance', 'dict': {'msg': msg}}))


def send_sub2(user_lin, banance, vtype):
    msg = upvictory(user_lin, banance, vtype)
    allconn.get(str(user_lin)).send(json.dumps({'type': 'banance', 'dict': {'msg': msg}}))


def websocket_log(request, user, room, user_lin):
    """处理前端发来的各种数据"""
    # try:
    for message in request.websocket:
        message = mess_log(message)
        print('收到信息', message)
        if not message:
            # 非正常退出游戏
            print(user)
            upvictory(user, 1, 0)
            if room.state == 'full' and user.userinfo.state == 'playing':
                print('给对方发信息')
                send_sub2(user_lin, 1, 1)
                out_room(user_lin)
                allconn.get(str(user_lin)).close()
                user_lin.userinfo.state = 'wait'
                user_lin.userinfo.save()

            auth_logout(request, user)
            allconn.pop(str(user))
            print(user, '已退出游戏')
            break

        elif message["type"] == 'close':
            # 正常退出websocket
            allconn.pop(str(user))
            request.websocket.close()
            if 'types' in message:
                # auth_logout(request, user)
                pass
            print(user, '已退出websocket')
            break

        elif message['type'] == 'message':
            # 聊天
            message_log(message, user, user_lin)

        elif message['type'] == 'request' or message['type'] == 'banance':
            if 'by' in message:
                if 'lose' in message['by']:  # 认输
                    send_sub1(request, user, 1, 0)
                    send_sub2(user_lin, 1, 1)
                    out_room(user)
                    request.websocket.close()
                    allconn.get(str(user_lin)).close()
                    out_room(user_lin)
                    break
                di = {'type': 'request', 'subtype': message['by']}
                di = json.dumps(di).encode('utf-8')
                allconn.get(str(user_lin)).send(di)
            elif 'subtype' in message:
                msg = message['msg']
                subtype = message['subtype']
                if subtype == 'draw' and msg:
                    # 同意求和
                    send_sub1(request, user, 3, 2)
                    send_sub2(user_lin, 3, 2)
                    out_room(user)
                    request.websocket.close()
                    allconn.get(str(user_lin)).close()
                    out_room(user_lin)
                    break
                elif subtype == 'wback' and msg:
                    # 同意悔棋
                    request.websocket.send(json.dumps({'type': 'wback'}))
                    allconn.get(str(user_lin)).send(json.dumps({'type': 'wback'}))
                    r = Current_Board.board.get(str(room.rnum))
                    if len(r.reco) >= 2:
                        uppermove(r)
                        uppermove(r)
                elif subtype == 'draw' and not msg:
                    # 拒绝求和
                    allconn.get(str(user_lin)).send(json.dumps({'type': 'request', 'subtype': 'false'}))
                elif subtype == 'wback' and not msg:
                    # 拒绝悔棋
                    allconn.get(str(user_lin)).send(json.dumps({'type': 'request', 'subtype': 'false'}))
                continue
            elif 'result' in message:
                result = message['result']
                print('输赢 : ', result)
                if result == 'lose':
                    print('lose')
                    send_sub1(request, user, 0, 0)
                elif result == 'win':
                    print('win')
                    send_sub1(request, user, 0, 1)
                break

        elif message['type'] == 'chess':
            # 下棋
            past = message['dic'].get("past")
            now = message['dic'].get("now")
            types = message['dic'].get("type")
            # 更新后端棋子位置
            nomove = thismove(past[0], past[1], now[0], now[1], types, str(room.rnum))
            if nomove:
                # 给对手发送消息
                two_user(past, now, types, user_lin)
            else:
                # 给自己回复消息
                one_user(now, past, types, request)
    # except Exception as e:
    #     print('异常信息: ', e)
    #     auth_logout(request, user)
    #     allconn.pop(str(user))
    #     print(user, '已退======出游戏')
