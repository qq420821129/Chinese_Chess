$(document).ready(function(){
    var s = $('#footer>.index').html()
    var enChange = s == 'first' ? true : false
    var side = $('#footer>.side') ? $('#footer>.side') : 'red'
    var full = false
    var timerID;
    function matchOther(){
        $.ajax({
            url: 'match_other',
            type: 'GET',
            dataType: 'json',
            data: {'access_token':cookie.get('access_token')},
            timeout:80*1000,
            success:function(data){
                d = $.parseJSON('data');
                if (d.result == 'OK'){
                    enChange = false;
                    full = true;
                    console.log('匹配成功');

                    $('.red').css({'left':'0',"display":'block'});
                    $('.black').css({'left':'0%',"display":'block'});

                    //交换按钮隐藏,准备按钮显示
                    $('.exchange').css('display','none');
                    $('.ready').css('display','block');
                    timerID = setInterval(function(){
                        $.ajax({
                            url: 'ready_start',
                            type: 'POST',
                            dataType: 'json',
                            data: {'side':side,'access_token':cookie.get('access_token')},
                            success:function(data){
                                d = $.parseJSON(data);
                                if (d['other'] == 'unready'){
                                    console.log('对方等待中')
                                }else{
                                    if (d['times'] == 60){
                                        clearInterval(timerID)
                                        full = false
                                        enChange = true
                                        window.location('/')
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
                console.log('utrl')
                window.location('/')
            }
        })
    }
    matchOther()
    $('.start').click(function(){
        clearInterval(timerID)
        $.ajax({
            url: 'start',
            type: 'post',
            dataType: 'json',
            data: {'side':side,'access_token':cookie.get('access_token')},
            timeout:1000*80,
            success:function(data){
                d = $.parseJSON(data);
                if (d.result == 'OK'){
                    $('form input').val(cookie.get('access_token'))
                    $('form').submit()
                }else if(d.other = 'out'){
                    matchOther()
                }
            },
            error:function(utrl){
                console.log(utrl)
                window.location('')
            }
        })
    })

    $('.exchange').click(function(){
        if (enChange && !full){
            side = side == 'red' ? 'black' : 'red'
            $('.red').attr('class','temp')
            $('.black').attr('class','red')
            $('.temp').attr('class','black')
            if(side == 'red'){
                $('.black').css('display','none')
                $('.red').css('display','0')
            }else{
                $('.red').css('display','none')
                $('.black').css('left','0')
            }
        }
    })

})