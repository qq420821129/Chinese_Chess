var cookie = {
    set:function(key,val,time){//设置cookie方法
        var date=new Date(); //获取当前时间
        var expiresDays=time;  //将date设置为n天以后的时间
        date.setTime(date.getTime()+expiresDays*24*3600*1000); //格式化为cookie识别的时间
        document.cookie=key + "=" + val +";expires="+date.toGMTString();  //设置cookie
    },
    get:function(key){//获取cookie方法
        /*获取cookie参数*/
        var getCookie = document.cookie.replace(/[ ]/g,"");  //获取cookie，并且将获得的cookie格式化，去掉空格字符
        var arrCookie = getCookie.split(";");  //将获得的cookie以"分号"为标识 将cookie保存到arrCookie的数组中
        var tips;  //声明变量tips
        for(var i=0;i<arrCookie.length;i++){   //使用for循环查找cookie中的tips变量
            var arr=arrCookie[i].split("=");   //将单条cookie用"等号"为标识，将单条cookie保存为arr数组
            if(key==arr[0]){  //匹配变量名称，其中arr[0]是指的cookie名称，如果该条变量为tips则执行判断语句中的赋值操作
                tips=arr[1];   //将cookie的值赋给变量tips
                break;   //终止for循环遍历
            }
        }
	},
      delete:function(key){ //删除cookie方法
         var date = new Date(); //获取当前时间
         date.setTime(date.getTime()-10000); //将date设置为过去的时间
         document.cookie = key + "=v; expires =" +date.toGMTString();//设置cookie

        return tips;
	}
};

$(document).ready(function(){
    var socket = new WebSocket("ws://" + window.location.host + "/chess/info");
    window.soc = socket;
    $('.out').click(function () {
        window.soc.send(JSON.stringify({"type":"close", 'types':'out'}));
        $.ajax({
            url: 'out',
            type: 'POST',
            async: false,
            success:function(data) {
                console.log(data);
                if (data) {
                    location.href = '/'
                }
            }})

    });

    var s = $('#footer>.index').html();
    var enChange = s == 'first' ? true : false;
    var full = false;
    var side = $('.side').val();
    col();
    function matchOther(){
        $.ajax({
            url: 'match_other',
            type: 'GET',
            dataType: 'json',
            data: {'uname':$('.hide_uname').val(),'room':$('.room').val()},
            success:function(data){
                d = eval("(" + JSON.stringify(data) + ")");
                console.log(d);
                if (d.result == 'OK'){
                    clearInterval(mtime);
                    enChange = false;
                    full = true;
                    console.log('匹配成功');
                    var other = d.other;

                    if (other){
                        $('.black>.nickName').html(other.username);
                        $('.black .victory>b').html(other.victory);
                        $('.black .defeat>b').html(other.defeat);
                        $('.black .draw>b').html(other.draw);
                        console.log(other);
                        console.log(other.score);
                        $('.black .score b').html(other.score)
                    }
                    $('.red').css({'left':'0',"display":'block'});

                    $('.black').css({'left':'0%',"display":'block'});
                    $('.start').css('display', 'block');
                    //交换按钮隐藏,准备按钮显示
                    $('.exchange').css('display','none');
                    $('.ready').css('display','block');
                    timerID = setInterval(function(){
                        $.ajax({
                            url: 'ready_start',
                            type: 'POST',
                            dataType: 'json',
                            data: {'side':side,'username':$('.hide_uname').val(),'room': $('.room').val()},
                            success:function(data){
                                d = eval("(" + JSON.stringify(data) + ")");
                                console.log(d);
                                if (d['other'] == 'unready'){
                                    console.log('对方等待中')
                                }else if(d['other'] == 'exit'){
                                    full = false;
                                    enChange = true;
                                    clearInterval(timerID);
                                    $('.black').css('left','50%');
                                    mtime = setInterval(matchOther,1000)
                                }else{
                                    if (d['times'] == 60){
                                        clearInterval(timerID);
                                        full = false;
                                        enChange = true;
                                        $('.black').css('left','50%');
                                        window.soc.send(JSON.stringify({"type":"close", 'types':'out'}));

                                        $.ajax({
                                            url: 'out',
                                            type: 'POST',
                                            async: false,
                                            success:function(data) {
                                                console.log(data);
                                                if (data) {
                                                    location.href = '/'
                                                }
                                            }})
                                    }
                                }
                            },
                            error:function(utrl){
                                console.log(utrl)
                            }
                        })
                    },1000)
                }
            },
            error:function(utrl){
                console.log(utrl);
                clearInterval(mtime);
                window.location.href = ('/')
            }
        })
    }
    var mtime = setInterval(matchOther,1000);
    $('.start').click(function(){
        console.log('------------------', timerID);
        $('.start').css('background', 'red');
        $('.start:hover').css('background','red');
        clearInterval(timerID);
        stimer = setInterval(function(){
            $.ajax({
            url: 'start',
            type: 'post',
            dataType: 'json',
            data: {'side':side,'username':$('.hide_uname').val(), 'room': $('.room').val()},
            timeout:1000*80,
            success:function(data){
                d = eval("(" + JSON.stringify(data) + ")");
                console.log(d);
                // alert();
                if (d.result == 'OK'){
                    console.log('开始成功');
                    clearInterval(stimer);
                    if (window.soc) {
                        window.soc.send(JSON.stringify({"type":"close"}));
                        window.soc.close()
                    }
                    // $('form input').val($('.hide_uname').html());
                    $('form').submit()

                }else if(d.other == 'exit'){
                    console.log('重新匹配');
                    $('.black').css('left','50%');
                    clearInterval(stimer);
                    $('.start').css({'background':'transparent', 'display': 'none'})
                    $('.start:hover').css('background', '#ff0000');
                    mtime = setInterval(matchOther,1000)
                }else{
                    // console.log(d.default)
                }
            },
            error:function(utrl){
                console.log('开始错误');
                console.log(utrl);
                window.location.href = ('')
            }
        })
        },1000)

    });

    function col(){
        if (enChange && !full){
            side = side == 'red' ? 'black' : 'red';
            $('.red').attr('class','temp');
            $('.black').attr('class','red');
            $('.temp').attr('class','black');
            if(side == 'red'){
                $('.black').css('display','none');
                $('.red').css('display','0')
            }else{
                $('.red').css('display','none');
                $('.black').css('left','0')
            }
        }
    }
    $('.exchange').click(function() {
        alert('hello');
        col()
    })
    // $('.out').click(function () {
    //     $.ajax({
    //         url:'loginout',
    //         type: 'GET',
    //         success:function(data){
    //             d = eval('(' + JSON.stringify(data) + ')');
    //             if (d.result = 'OK'){
    //                 location.href = '/'
    //             }else{
    //                 console.log(d)
    //             }
    //         }
    //     })
    // })

});
