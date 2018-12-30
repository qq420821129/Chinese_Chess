

//这是一个对象，用来做本地存储的
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
        return tips
	},
      delete:function(key){ //删除cookie方法
         var date = new Date(); //获取当前时间
         date.setTime(date.getTime()-10000); //将date设置为过去的时间
         document.cookie = key + "=v; expires =" +date.toGMTString();//设置cookie
	}
};


//页面加载前调用
$(document).ready(function(){
    if (cookie.get("remember") == "true"){
        $("#account").val(cookie.get("user"));
        $("#passwd").val(cookie.get("passwd"));
        $("#check a").css("background","url('images/backimg.png')").css('background-position',"-59px -17px");
        $("#check a").attr("hasClick",true)
    }
	//改变登录方式选择样式
    function changeType(base,other){
        base.attr("shaddow",false);
        base.css("color","black");
        other.attr("shaddow",true);
        other.css("color","gray").mouseenter(function(){
            $(this).css("color","black");
        }).mouseleave(function(){
            if ($(this).attr("shaddow") == "true"){
                $(this).css("color","gray");
            }
        });
    }

    // 登录模式切换
    $(".login_n").click(function(){
        changeType($(this),$(".login_e"));
        $("#login_n").css("display","block");
        $("#login_e").css("display","none");
    });
    $(".login_e").click(function(){
        changeType($(this),$(".login_n"));
        $("#login_e").css("display","block");
        $("#login_n").css("display","none");
    });
    $(".login_n").click();

    // 账号密码设置切换关注效果
    $("#account").focus(function(){
        $(this).attr("class","form-control change")
    }).blur(function(){
        $(this).attr("class","form-control")
    }).keydown(function(e){
		var key = e["originalEvent"]["key"];
        if($(this).val().length == 16){
            if(e["originalEvent"]["key"] != "Backspace"){
                e.preventDefault();
            }
        }
    });
    $("#passwd").focus(function(){
        $(this).attr("class","form-control change");
    }).blur(function(){
        $(this).attr("class","form-control");
    }).keydown(function(e){
        if($(this).val().length == 16){
            if(e["originalEvent"]["key"] != "Backspace"){
                e.preventDefault();
            }
        }
    });

	//检测是否记住密码
    $("#check a").click(function(e){
        b = eval($(this).attr("hasClick"));
        $(this).attr("hasClick",!b);
        console.log();
        if (!b){
            $(this).css("background","url('images/backimg.png')").css('background-position',"-59px -17px");
			cookie.set("remember",true,7)
        }else{
            $(this).css("background","");
			cookie.delete("remember");
			localStorage.setItem("access_token","")
        }
    });
    $("#check span").click(function(){
        $("#check a").click()
    });

	//获取本地access_token
	function getToken(){
		var key = "access_token";
		return cookie.get(key)
	}
	
	//验证后进行登录到主页
	function loginMethod(access_token){
		// $.ajax({
		// 			url:"login_home",  // 进入游戏
		// 			type:"POST",
		// 			dataType:"json",
		// 			data:{"access_token":cookie.get("access_token")},
		// 			success:function(data){
		// 			// d = eval("(" + JSON.stringify(data) + ")");
		// 			if (data == "OK"){
		// 			    console.log(data);
		// 				return true
		// 			}else{
		// 				alert("服务器错误")
  //                       return false;
		// 			}
		// 		}
		// })
        input = document.createElement('input');
        input.display = 'hidden';
        input.name = 'access_token';
        input.value = access_token; //appendChild
        $('form').append(input);
        $('form').submit()
	}
	
	$("#nickN").keydown(function(e){
        if($(this).val().length === 16){
            if(e["originalEvent"]["key"] != "Backspace"){
                e.preventDefault();
            }
        }
    });
	$("#loginNoPass").click(function(e){
	    e.preventDefault();
		var usr = $("#nickN").val();
		if (/^[_a-zA-Z0-9]{5,16}$/.test(usr)){
			$.ajax({
				url:"login_auth",  // 游客登录
				type:"POST",
				dataType:"json",
				data:{"nickN":usr,"ID":0},
				success:function(data){
				    console.log(data);
					d = eval("(" + JSON.stringify(data) + ")");
					cookie.set("tmpToken",d["access_token"],1);
					window.open("home1.html")
				},
                error:function(e){
                    console.log("NO passwd login:",e)
                }
			})
		}else{
			$("#tips").html("昵称中不得包含特殊字符")
		}
	});
	
	//登录按钮
    $("button").click(function(e){
		if (getToken()){
			loginMethod(cookie.get('access_token'))
		}else{
        var user = $("#account").val();
        var passwd = $("#passwd").val();
        var u = /^[_a-zA-Z0-9]{5,16}$/;
        var p = /^[a-zA-Z][_a-zA-Z0-9]{3,15}$/;
        if (u.test(user) && p.test(passwd)){
            var keepKey = false;
            if ($("#check a").attr("hasClick") === "true"){
                cookie.set("user",user,7);
				cookie.set("passwd",passwd,7)
            }
            $.ajax({
				url:"static_auth",  //登录游戏
				type:"POST",
				dataType:"json",
				data:{"usr":user,"psw":hex_sha1(passwd),"hasAuth":false,"ID":1},

				success:function(data)
                {
                    console.log(data);
				    d = eval("(" + JSON.stringify(data) + ")");
				    if (cookie.get("remember") == "true")
				    {
					   cookie.set("access_token",d["access_token"],7)
				    }
				    console.log(d["access_token"]);
				    loginMethod(d['access_token'])
			    },
				error:function(e){
					d = eval("(" + JSON.stringify(e) + ")");
					$("#tips").html(d.responseText).css('display','block');
                    $("#tips").css("display","inline");
                    setTimeout(function(){
                        $("#tips").css("display","none");
                    }, 3000);
                    return false
				}
			})

        }else{
            if (user.length < 4){
                $("#tips").html("用户名不得低于4位")
            }else if(user.length > 16){
                $("#tips").html("用户名不得大于16位")
               }else{
                $("#tips").html("用户名中不得包含除下划线外的其他字符")
            }
            if (passwd.length < 6){
                $("#tips").html("密码不得低于4位")
            }else if(passwd.length > 16){
                $("#tips").html("密码不得大于16位")
            }else if (!/^[A-Za-z]$/.test(passwd.substr(0,1))){
                $("#tips").html("密码需以字母开头")
            }
            $("#tips").css("display","inline");
            setTimeout(function() {
                $("#tips").css("display","none");
            }, 3000);
            return false;
        }}
        return false
    });
}
);

