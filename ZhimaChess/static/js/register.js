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
        var arrCookie = getCookie.split(";")  //将获得的cookie以"分号"为标识 将cookie保存到arrCookie的数组中
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
}




// $.validator.setDefaults({
// 	submitHandler:function(form){
// 		form.submit()
// 	}
// });


$(document).ready(function(){
	var encrypt = new JSEncrypt()
	encrypt.setPublicKey(null)
	
	var validator = $("form").validate({
		submitHandler:function(form){
		    form.commit()
		},
        rules:{
                userName:{
                    required:true,
                    remote:{
                        type:"post",//数据请求方式
                        url:"test",//异步验证路径
                        data:{
                            "userName":$("#usr").val()
                        },
                        dataType:"json",
                        success:function(data,type){//AJAX异步返回数据
                            data = eval("("+data+")");
                            if(data.state){
                                return true;
                            }else{
                                return false;
                            }
                        },
                        error:function(e){
                            return false;
                        }
                    }
                }
        },
        message:{
            userName:{
                remote:"已经注册"
            }
        }
        
    });
    $("#reset").click(function(){
            validator.resetForm()
    })

    
    


	$("input").focus(function(event) {
		$(this).attr("class","change")
	}).blur(function(event) {
		$(this).attr("class","")
	});;

});