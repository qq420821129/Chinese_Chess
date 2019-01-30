
window.onbeforeunload = function(e){
    $.ajax({
        url:'/',
        type: 'get',
        data: {'status':'exit'},
        async:false,
    })
}

function connectServer(){
    clearInterval(timeId)
    var socket = new WebSocket("ws://" + window.location.host + "/playground/server");
    window.soc = socket;
    soc.onmessage = function(event){
        var result = event.data
        var dic = result.dict;
        var type = result['type']
        if (type === 'info'){   // 用于状态交互
            if (dic['toRoom']){
                soc.send('close')
                window.location.href = 'match'
            }
        }else if (type === 'init' || type === 'update') {    // 获取初始房间和用户数据
            // 首先用户进入房间一次拉取所有房间状态信息,然后就针对之后的用户改变房间状态时服务器主动推送update到其他用户的套接字中
            updateInfo()
        } else if(type === 'msg'){  // 提示信息,例如连接成功,失败
            $('msg info').html(dic['content'])
        }
    }
}

function updateInfo(){
    rooms = dic['rooms']
    for (var i = 0; i < rooms.length; i++){
        room = rooms[i]
        setTableWithRoom(room)
    }
    users = dic['users']
    for (var i = 0; i<users.length;i++){
        var user = users[i]
        setRightWithUser(user)
    }
}

function setRightWithUser(user){
    if (user.status == 'online') {
        var li = document.createElement('li')
        li.setAttribute('id', user.id)
        var div = document.createElement('div')
        div.setAttribute('class', 'uname')
        div.innerHTML = user.username
        li.append(div)
        if (user.room) {
            var div1 = document.createElement('div')
            div1.setAttribute('class', 'utable')
            div1.innerHTML = 'user.room'
            li.append(div1)
        }
        $('#user_list>ul').append(li)
    }else if(user.status == 'offline'){
        $('#user_list>ul').remove($('#' + user.id))
    }
}

function keyAlive(){
    timeId = setInterval(function(){
        $.ajax({
            url:'playground/keepAlive',
            type:'get',
            dataType:'json',
            cache:false,
            success:function(data){
                console.log('alive')
                if(data.status == 'back'){
                    connectServer()
                }
            }
        })
    },1000)

}

$(document).ready(()=>{
    connectServer()
    $('.table_face').on('click',function(){
        li = $(this).parents('li')[0]
        rid = $(li).attr('id')
        side = $($(this).parent('div')[0]).attr('class') == 'table_l' ? 'red' : 'black'
        soc.send(JSON.stringify({'type':'match','room':rid,'side':side}))
    })
})


// 需求数据 rooms red   black
// 后台需要缓存数据到内存中
function getCicyle(){
    $.ajax({
        url: 'playground/info',
        type: 'get',
        dataType: 'json',
        cache: false,
        success:function(data){
            $('.conninfo').show()
            var rooms = data['rooms']
            for (var i=0; i<rooms.length; i++){
                room = rooms[i]
                if (room.state === 'playing'){
                    $('#'+room.id + '>.table_c p').show()
                }else{
                    $('#'+room.id + '>.table_c p').hide()
                }
                setTableWithRoom(room)
            }

        },
        error:function (err) {
            console.log(err)
        }
    })
}

function setTableWithRoom(room) {
    if (room.state === 'playing'){
        $('#'+room.id + '>.table_c p').show()
    }else{
        $('#'+room.id + '>.table_c p').hide()
    }
    if (room.red){
        $('#' + room.id + '_2s>img').show()
        $('#' + room.id + '>table_l>table_name>span').html(room.red.username)
    }else{
        $('#' + room.id + '_2s>img').hide()
        $('#' + room.id + '>table_l>table_name>span').html('')
    }
    if (room.black){
        $('#' + room.id + '_1s>img').show()
        $('#' + room.id + '>table_r>table_name>span').html(room.red.username)
    }else{
        $('#' + room.id + '_1s>img').hide()
        $('#' + room.id + '>table_r>table_name>span').html('')
    }
}
