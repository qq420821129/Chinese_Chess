


# 得到前端请求的桌号, 例 5 号


# 判断桌号是否存在与全局字典 interactive 中

# 如果不存在则新增 interactive['5'] = [false, []] 值分别对应 红方, 黑方, 棋盘

# 每位玩家都有 false/true 两种状态, false为当前下棋玩家, true为等待对手下棋, 当一方下完棋后就将两方状态置反, 进入等待另一方下棋

# 第一位进入该桌号的

