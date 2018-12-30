$(document).ready(function(){
    S = parseInt($('#side').html());
    console.log(S);
    loadMap();
    putDef();
    showC();
    if (S === -1){
        $.ajax({
            url: 'chess/info',
            type: 'GET',
            dataType: 'json',
            success:function(data){
                var r = JSON.parse(data);
                runNow = true;
                onMove = false;
                past = r['past'];
                now = r['now'];
                type = r['type'];
                onChose(past[0],past[1],type);
                onChose(now[0],now[1],type)
            }
        })
    }else{
        runNow = true
    }
});

function waitOther(dict){
    onMove = true;
    $.ajax({
        url: 'chess/info',
        type: 'GET',
        dataType: 'json',
        data: dict,
        success:function(data){
            var r = JSON.parse(data);
            if (r['end']){
                runNow = false;
                Log('失败处理')
            }else{
                onMove = false;
                past = r['past'];
                now = r['now'];
                type = r['type'];
                onChose(past[0],past[1],type);
                onChose(now[0],now[1],type)
            }
        },
        error:function(e){
            LogError(e,'POSITION ERROR')
            return
        }
    })
}

//数组拓展方法,   暂时没用
Array.prototype.MyPush = function(d){
    if (this.length>=10){
        this.shift()
    }
    this.push(d)
}

//加载地图数组
function loadMap(){
    for(var j=0;j<10;j++){
        map[j] = []
        for(var i=0;i<9;i++){
            map[j][i] = 0
        }
    }
}

// 打印方法
function Log(info){
    if(DeBug){
        console.log("DEBUG:"+info);
    }
}
function LogError(info){
    if(DeBug){
        console.log("ERROR:"+info);
    }
}

//动态布置棋子
function showC(){
    for(var j=0;j<10 ;j++) {
        for (var i = 0; i < 9; i++) {
            var cla="";
            var tex="";
            var isNone=false;
            var T=getCText(j,i);
            if(T == null){
                isNone=true;
            }else{
                cla=T[1];
                tex=T[0];
            }
            if(isNone){
                continue;
            }
            var c = map[j][i]
            if(c > 0){
                cla = 'D ' + cla
            }else{
                cla = 'U ' + cla
            }
            $("#CS"+j+"-"+i).html(
                    "<section class='C "+cla+"'>"+tex+"</section>"
            )
        }
    }
    Log("完成显示场景");
}


//0空
//兵1 炮2 车3 马4 相5 士6 将7 红
//卒-1 炮-2 车-3 马-4 象-5 士-6 帅-7 黑

//填充数组
function putDef(){
    map[0][0]=-3*S; map[9][0]=3*S;  // y,x  j,i
    map[0][1]=-4*S; map[9][1]=4*S;
    map[0][2]=-5*S; map[9][2]=5*S;
    map[0][3]=-6*S; map[9][3]=6*S;
    map[0][4]=-7*S; map[9][4]=7*S;
    map[0][5]=-6*S; map[9][5]=6*S;
    map[0][6]=-5*S; map[9][6]=5*S;
    map[0][7]=-4*S; map[9][7]=4*S;
    map[0][8]=-3*S; map[9][8]=3*S;

    map[2][1]=-2*S; map[7][1]=2*S;
    map[2][7]=-2*S; map[7][7]=2*S;
    map[3][0]=-1*S; map[6][0]=1*S;
    map[3][2]=-1*S; map[6][2]=1*S;
    map[3][4]=-1*S; map[6][4]=1*S;
    map[3][6]=-1*S; map[6][6]=1*S;
    map[3][8]=-1*S; map[6][8]=1*S;
    Log("完成放置默认棋子");
}

//查找当前点的具体情况
function WhatSpace(y,x){
    return map[y][x]
}

var runNow = false

var map = []
var DeBug = true

// OnDoing
var onMove = false
var OnChoseNow = false
var nowChoseC = []
var nowWho = 0  //0红 1黑
var moveList = []
var eatList = []

//清除选择样式
function cleanChose(){
    $(".CS").css({
        "box-shadow": "",
        "border": ""
    })
}

//清除选择状态
function cleanSt(){
    nowChoseC = []  //当前选择的棋子
    cleanChose()    //清除选择样式
    moveList = []   //可移动的列表
    eatList = []    //可以吃的列表
    OnChoseNow = false  //当前是否在选择中
}

//选择某位置
function onChose(j,i){
    if (!runNow) 
        return
    if (onMove) 
        return
    //获取该点是空点还是棋子
    var CC = WhatSpace(j,i)
    if(CC==0){
        //选择的是空点
        onChoesS(j,i)
    }else{
        //选择棋子
        Log('选择了' + j + '-' + i + ' ' + CC)
        onChoseC(j,i,CC)
    }
}

//选择棋子  t  0=空点 -=黑棋 +=红棋
function onChoseC(j,i,t){ 
    //如果现在不是选择状态
    if(!OnChoseNow){
        //如果下棋人不符则直接返回
        if (nowWho==0){
            if(t<0)
                return
        }
        if (nowWho>0){
            if(t>1)
                return
        }
    }
    //如果选择放回原位
    if (nowChoseC[0]==j&&nowChoseC[1]==i){
        //清除状态,结束
        cleanSt()
        return
    }
    //如果当前是选择状态
    if(OnChoseNow==true){
        //遍历可吃列表,如果是要吃子,进行吃子操作
        for(var q=0;q<eatList.length;q++){
            if (eatList[q][0]==j&&eatList[q][1]==i){
                eat(nowChoseC[0],nowChoseC[1],j,i)  //移动并吃子
                break
            }
        }
        //清除状态,结束
        cleanSt()
    }
    //如果下棋人不符,清除
    if (nowWho==0) {  //红棋
        if (t<0){ //t<0 黑棋
            cleanSt()
            return
        }
    }
    if (nowWho>0){ //黑棋
        if(t>0){  //红棋
            cleanSt()
            return
        }
    }
    // 显示当前可走路径
    showSt(j,i,t);
}

//换边
function trunH(){
    if(nowWho==0){
        nowWho=1;
    }else{
        nowWho=0;
    }
    cleanSt();
}


//0空
//兵1 炮2 车3 马4 相5 士6 将7 红
//卒-1 炮-2 车-3 马-4 象-5 士-6 帅-7 黑
function WhereCan(y,x,t){//-黑棋 +红棋
    var c=0;
    if(t<=0){
        c=1;
        t*=-1;
    }
    var tmap=[];
    switch (t){ //t为棋子类型  c 0位红棋 1为黑棋
        case 1:
            binMove(tmap,c,y,x);    //兵移动可能性
            break;
        case 2:
            paoMove(tmap,c,y,x);    //炮移动可能性
            break;
        case 3:
            juMove(tmap,c,y,x);     //車移动可能性
            break;
        case 4:
            maMove(tmap,c,y,x);     //馬移动可能性
            break;
        case 5:
            xiangMove(tmap,c,y,x);  //相移动可能性
            break;
        case 6:
            shiMove(tmap,c,y,x);    //仕移动可能性
            break;
        case 7:
            JSMove(tmap,c,y,x);     //帅移动可能性
            break;
        default :
            break;
    }

    for(var l=0;l<tmap.length;l++){

        if(CanEat(tmap[l][0],tmap[l][1],c)){  //c 0红棋 1黑棋
            tmap[l][2]=1;
        }else{
            tmap[l][2]=0;
        }
    }
    return tmap;
}

//判断是否可以吃子 c 0 红棋 1黑棋 不能吃的为空子或者同类
function CanEat(y,x,c){
    var cc=0;
    if(c==0){
        cc=1; //cc 1为红棋 -1位黑棋
    }else{
        cc=-1;
    }
    //黑棋为负 * 红棋 < 0 所以可吃,反之一样 0 * cc == 0
    return map[y][x]*cc<0;
}

//显示当前可走路径
function showSt(j,i,t){
    nowChoseC = []  //清空当前选择列表
    cleanChose()    //先清除自身样式
    showChose(j,i,1)  //改变自身显示样式
    var tmap = WhereCan(j,i,t*S)  //t 0空点 +红棋 -黑棋
    //统计当前可以走的路径
    if(tmap!=null&&tmap.length>0){
        for (var q=0;q<tmap.length;q++){  //遍历当前可移动路径
            if (map[tmap[q][0]][tmap[q][1]]==0) {  //如果该点为空点
                moveList.push(tmap[q])  //添加到可移动列表中
            }else{
                eatList.push(tmap[q])  //添加到可吃列表中
            }
            //提示可选路径样式
            showChose(tmap[q][0],tmap[q][1],tmap[q][2]+2)
        }
    }
    // 将棋子信息保存在列表中
    nowChoseC[0] = j
    nowChoseC[1] = i
    nowChoseC[2] = t
    OnChoseNow = true   //设置当前已经选择棋子
}

//0清除 1绿色 2黄色 3红色  提示可移动路径样式
function showChose(j,i,t){
    //获取当前的空格
    var o=$("#CS"+j+"-"+i);
    //如果是清除样式,清除
    if(t==0){
        o.css({
            "box-shadow": "",
            "border": ""
        });
        return;
    }
    var c="";
    switch (t){
        case 1:     //被选中的棋子为绿色边框
            c="6bc274";
            break;
        case 2:     //可走路径为黄色边框
            c="eeb948";
            break;
        case 3:     //可吃的子为红色边框
            c="c53f46";
            break;
        default :
            break;
    }
   o.css({
        "box-shadow": "0 0 25pt #"+c,
        "border": "3px solid #"+c
    })
}

//选中空位
function onChoesS(j,i){
    if(OnChoseNow){
        //如果当前是选择状态,且可移动列表中有该点则移动到该点
        for(var q=0;q<moveList.length;q++){
            if (moveList[q][0]==j&&moveList[q][1]==i){  //如果移动列表中有该点坐标
                move(nowChoseC[0],nowChoseC[1],j,i) //移动到该点  不能吃
                break
            }
        }
    }
    cleanSt()
}


function getCText(j,i){
    var T=[];
    switch (map[j][i])
     {
     case (0):
        return null;
     break;
     case (1):
         T[0]="兵";
         T[1]="BR";
     break;
     case (2):
         T[0]="炮";
         T[1]="PR";
     break;
     case (3):
         T[0]="車";
         T[1]="JR";
     break;
     case (4):
         T[0]="馬";
         T[1]="MR";
     break;
     case (5):
         T[0]="相";
         T[1]="XR";
     break;
     case (6):
         T[0]="仕";
         T[1]="SR";
     break;
     case (7):
         T[0]="帅";
         T[1]="J";
     break;
     case (-1):
         T[0]="卒";
         T[1]="BB";
     break;
     case (-2):
         T[0]="砲";
         T[1]="PB";
     break;
     case (-3):
         T[0]="車";
         T[1]="JB";
     break;
     case (-4):
         T[0]="馬";
         T[1]="MB";
     break;
     case (-5):
         T[0]="象";
         T[1]="XB";
     break;
     case (-6):
         T[0]="士";
         T[1]="SB";
     break;
     case (-7):
         T[0]="将";
         T[1]="S";
     break;
     default :
         return null;
     break;
     }
    return T;
}

//移动具体实现
function move(y,x,j,i,eat){
    onMove=true;    //移动状态改为true
    var dest = (map[j][i] == 7 || map[j][i] == -7);
    var end = false
    if(eat==null)   //如果不能吃子,但是该点又不为空,不与移动报错
        if(dest!=0){
            LogError("错误的位置");
            return;
        }
    var cla="";
    var tex="";
    var T=getCText(y,x);    //获取该点棋子
    if(T == null){  //如果获取不到,报错丢失棋子
        LogError("丢失棋子信息");
        return;
    }else{  //获取棋子的坐标和
        cla=T[1];   //获取棋子的代号和名称
        tex=T[0];
    }
    //获取当前的类,分辨颜色
    var c = map[y][x]
    if(c > 0){
        cla = 'D ' + cla
    }else{
        cla = 'U ' + cla
    }

    if(eat==null)   //如果不能吃子,打印移动信息
        Log(y+"-"+x+" "+tex+" 移动到"+j+"-"+i);
    else    //可以吃子打印吃子信息
        Log(y+"-"+x+" "+tex+" 吃"+j+"-"+i+" "+getCText(j,i)[0]);
        if (dest){
            end = true;
        }
    map[j][i]=map[y][x];    //移动到新位置
    map[y][x]=0;            //清空原位置
    $("#CS"+j+"-"+i).html(  //标签更新
            "<div class='C "+cla+"' style='transform:translate("+(x-i)*45+"px,"+(y-j)*45+"px);'>"+tex+"</div>"
    );
    $("#CS"+y+"-"+x).html(""); //原位置删除标签
    setTimeout(function(){
        $("#CS"+j+"-"+i+" div").css({   //新位置棋子去除形变特效
            transform:""
        })
    },10);
    
    setTimeout(function(){  //换边
        trunH();
        if (!end){
            dic = {'past': [y,x],
                'now':[j,i],
                'type':map[j][i]
                };
            waitOther(dic)
        }else{
            onMove = false;
            runNow = false;
            $.ajax({
                url: 'chess/end',
                type: 'POST',
                dataType: 'json',
                data: {'winner':S},
                success:function(){
                    Log('成功处理')
                },
                error:function(){
                    Log('失败处理')
                }
            })
        }
    },700);
}

//吃子
function eat(y,x,j,i){
    onMove=true;
    $("#CS"+j+"-"+i+" div").css({
        transform:"scale(0,0)"
    })  //目标位置标签变为0
    var end = Math.abs(map[j][i]) == 7
    setTimeout(function(){
        move(y,x,j,i,true);//可以吃子的移动
        console.log('end:',end)
    },0)
}

//兵的移动路径可能性
function binMove(tmap,c,y,x){//0红 1黑    tmap保存棋子可移动的可能性
    var w;      //保存小兵是否过河
    var h=0;    //保存方向  -1为上,1为下
    if(c==0){       //红方
        w=y<5;
        h=-1;
    }else{          //黑方
        w=y>4;
        h=1;
    }
    if(w){          //如果小兵过河 方向任意
        if(y+h>=0&&y+h<map.length){     //小兵向任意方向走一步
            //小兵往前走
            var t1=[];
            t1[0]=y+h;
            t1[1]=x;
            tmap.push(t1);
        }
        //小兵横向走,-1为左,1为右
        var t2=[];var t3=[];
        t2[0]=y;t3[0]=y;
        t2[1]=x-1;t3[1]=x+1;
        tmap.push(t2);tmap.push(t3);
    }else{      //小兵没有过河,只能往前走一步
        var t=[];
        t[0]=y+h;
        t[1]=x;
        tmap.push(t);
    }
    console.log(tmap)   
}

//炮移动 
function paoMove(tmap,c,y,x){   //c为0红 1黑 0上1左2下3右
    // 统计上下左右四个方向可能性
    paoMove_(tmap,0,c,y,x);
    paoMove_(tmap,1,c,y,x);
    paoMove_(tmap,2,c,y,x);
    paoMove_(tmap,3,c,y,x);
}

//炮移动  d为方向  0上1左2下3右
function paoMove_(tmap,d,c,y,x){//0上1左2下3右
    var q= y,w= x,qi= 0,wi= 0,ci=0;//ci:0红 1黑
    if(c==0){ 
        ci=1; //红
    }else{
        ci=-1; //黑
    }
    var cc;
    switch (d){
        case 0:
            cc=function(q){return q>=0;}    //q y轴位置
            qi=-1;   //qi向上
            break;
        case 1:
            cc=function(q,w){return w>=0;}  //w x轴位置
            wi=-1;  //wi向左
            break;
        case 2:
            cc=function(q){return q<map.length;} //q小于地图最下边
            qi=1;   //qi向下
            break;
        case 3:
            cc=function(q,w){return w<map[0].length;}  //w小于地图最右边
            wi=1;   //wi向右
            break;
    }
    var ce=false; //ce用来判断是否隔子,隔子为True
    while(true){
        if(!cc(q,w))break;  //如果方向d设置错误,或者y,x超出范围,则什么也不做
        if(q==y&&w==x){     //从点击位置开始往d方向往前一步判断
            q+=qi;w+=wi;
            continue;
        }
        if(map[q][w]==0){   //如果该点是空点
            if(!ce){      //ce用来判断是否隔子,隔子为True
                var t=[];  //没隔子的空点直接添加到可行路径中
                t[0]=q;
                t[1]=w;
                tmap.push(t);
            }
        }else{      //如果该点有棋子
            if(ce){     //如果是之前还没有隔子,则跳过不执行
                if(map[q][w]*ci<0){ //如果已经隔子则判断该棋子是否对方棋子,是则添加到可行路径
                    var t=[];
                    t[0]=q;
                    t[1]=w;
                    tmap.push(t);
                    ce=false;   //重置隔子变量,并退出循环
                    break;
                }
            }
            ce=true;    //如果是之前还没有隔子,在不执行操作后设置已经隔子
        }
        q+=qi;w+=wi;    //步长进1
    }
}

//車移动路径 c为0红1黑 y为竖直方向,x为水平方向
function juMove(tmap,c,y,x){
    //分上左下右四个方向分别进行计算
    for(var q=y;q>=0;q--){
        if(q==y)continue;
        if(!fastMove(tmap,c,q,x))break;
    }
    //向左遍历
    for(var q=x;q>=0;q--){
        if(q==x)continue;
        if(!fastMove(tmap,c,y,q))break;
    }
    //向下遍历
    for(var q=y;q<map.length;q++){
        if(q==y)continue;
        if(!fastMove(tmap,c,q,x))break;
    }
    //向右遍历
    for(var q=x;q<map.length;q++){
        if(q==x)continue;
        if(!fastMove(tmap,c,y,q))break;
    }
}

//車移动子方法
function fastMove(tmap,c,y,x){//c:0红 1黑
    var ci=0;
    if(c==0){
        ci=1;   //红
    }else{
        ci=-1;  //黑
    }
    if(map[y][x]==0){   //如果是空点
        var t=[];
        t[0]=y;
        t[1]=x;
        tmap.push(t);   //直接添加到可行路径中
        return true;
    }else{      //如果不是空点
        if(map[y][x]*ci<0){ //如果是对方棋子,添加到可行路径中
            var t=[];
            t[0]=y;
            t[1]=x;
            tmap.push(t);
        }
        return false;   //不管是否对方棋子,碰到棋子后此方向都结束计算
    }
}

//馬移动规则
function maMove(tmap,c,y,x){
    //馬移动子方法
    function fastMa(tmap,y,x,ys,xs,c){
        if(y+ys<map.length&&y+ys>=0&&x+xs<map.length&&x+xs>=0)  //确保在棋子四个方向没有超出地图范围
        if(map[y+ys][x+xs]==0){ //如果在馬的某个方向隔壁位置有棋子,则什么都不做,蹩脚
            var yz= 0,xz=0; //设置馬在y和x轴的偏移辆
            if(ys==0){  //如果是x轴方向的行动,则在y轴偏移正负1
                yz=-1;
            }else{      //如果是y轴方向的行动,则在x轴偏移正负1
                xz=-1;
            }
            // 以yz=-1为例,即y轴的方向位移为1  
            if(y+ys+ys-yz<map.length&&y+ys+ys-yz>=0&&x+xs+xs-xz<map.length&&x+xs+xs-xz>=0)//判断是否超出范围
            if(map[y+ys+ys-yz][x+xs+xs-xz]*c<=0){   //如果该点有对方棋子或者为空点
                var t=[];
                t[0]=y+ys+ys-yz;
                t[1]=x+xs+xs-xz;
                tmap.push(t);   //添加到可移动路径
            }
            // 以yz=-1为例,即y轴的方向位移为1 与上个if方向相反
            if(y+ys+ys+yz<map.length&&y+ys+ys+yz>=0&&x+xs+xs+xz<map.length&&x+xs+xs+xz>=0)//判断是否超出范围
            if(map[y+ys+ys+yz][x+xs+xs+xz]*c<=0){   //如果该点有对方棋子或者为空点
                var t1=[];
                t1[0]=y+ys+ys+yz;
                t1[1]=x+xs+xs+xz;
                tmap.push(t1);  //添加到可移动路径
            }
        }
    }
    var cc=0;
    if(c==0){   //红
        cc=1;
    }else{      //黑
        cc=-1;
    }
    fastMa(tmap,y,x,-1,0,cc);   //往上判断
    fastMa(tmap,y,x,1,0,cc);    //往下判断
    fastMa(tmap,y,x,0,-1,cc);   //往左判断
    fastMa(tmap,y,x,0,1,cc);    //往右判断
}

//相移动路径计算
function xiangMove(tmap,c,y,x){//c:0红 1黑
    //相移动路径计算子方法
    function fastXiang(tmap,y,x,yy,xx,c,cy){
        if(y+yy*2<map.length&&y+yy*2>=0&&x+xx*2<map.length&&x+xx*2>=0){//棋子不超出地图位置
            if(cy(y+yy*2))  //如果位置已经过河则什么都不做
            if(map[y+yy][x+xx]==0){ //如果移动方向的中间为空点,即不蹩脚才继续,否则不予计算
                if(map[y+yy*2][x+xx*2]*c<=0){   //如果落子地方为空或者对方棋子才添加路径
                    var t=[];
                    t[0]=y+yy*2;
                    t[1]=x+xx*2;
                    tmap.push(t);
                }
            }
        }
    }
    var cc=0;
    if(c==0){   //红方
        cc=1;
    }else{
        cc=-1;  //黑方
    }
    var ch;
    if(c==0){
        ch=function(y){return y>4};   //相不能过河,红方在下方
    }else{
        ch=function(y){return y<5};   //相不能过河,黑方在上方
    }
    //分四个方向判断
    fastXiang(tmap,y,x,1,1,cc,ch);  //右下
    fastXiang(tmap,y,x,1,-1,cc,ch); //左下
    fastXiang(tmap,y,x,-1,1,cc,ch); //右上
    fastXiang(tmap,y,x,-1,-1,cc,ch);    //左上
}

//士移动路径
function shiMove(tmap,c,y,x){//c:0红 1黑
    //士移动路径子方法
    function fastShi(tmap,y,x,yy,xx,c,cc){

        if(cc(y+yy)){   //如果竖直方向不超过上下三行
            if(x+xx>=3&&x+xx<=5){   //如果横向在第四行和第六行之间
                if(map[y+yy][x+xx]*c<=0){   //如果目标点是空点或者有地方棋子
                    var t=[];
                    t[0]=y+yy;
                    t[1]=x+xx;
                    tmap.push(t);   //保存到数组中
                }
            }
        }
    }
    var cf;
    var cc=0;
    if(c==0){   //红
        cc=1;
        cf=function(y){return y>=7&&y<=9}   //红方只能在最下面三行
    }else{      //黑
        cf=function(y){return y>=0&&y<=2}   //黑方只能在最上面三行
        cc=-1;
    }
    fastShi(tmap,y,x,1,1,cc,cf);    //右下方
    fastShi(tmap,y,x,-1,1,cc,cf);   //右上方
    fastShi(tmap,y,x,1,-1,cc,cf);   //左下方
    fastShi(tmap,y,x,-1,-1,cc,cf);  //左上方
}

//老帅移动
function JSMove(tmap,c,y,x){
    //老帅移动快捷方法
    function fastJS(tmap,y,x,yy,xx,c,cc){
        if(cc(y+yy)){   //如果竖直方向在各自的帅格内
            if(x+xx>=3&&x+xx<=5){   //如果水平方向也在帅格内
                if(map[y+yy][x+xx]*c<=0){   //如果目标点是空点或者有地方棋子
                    var t=[];
                    t[0]=y+yy;
                    t[1]=x+xx;
                    tmap.push(t);   //添加到可移动路径
                }
            }
        }
    }
    var cf;
    var cc=0;
    if(c==0){   //红
        cc=1;
        cf=function(y){return y>=7&&y<=9}   //红方老帅竖直在下三行
    }else{      //黑
        cf=function(y){return y>=0&&y<=2}   //黑方老帅竖直在上三行
        cc=-1;
    }
    fastJS(tmap,y,x,1,0,cc,cf);     //往下判断
    fastJS(tmap,y,x,-1,0,cc,cf);    //往上判断
    fastJS(tmap,y,x,0,-1,cc,cf);    //往左判断
    fastJS(tmap,y,x,0,1,cc,cf);     //往右判断
    if(c==0){
        for(var q=y-1;q<map.length&&q>=0;q--){  //红方对帅上方各点遍历
            if(map[q][x]==0){   //如果为空点继续遍历
                continue;
            }
            if(map[q][x]==-7){  //如果遇到点为对方老帅
                var t=[];
                t[0]=q;
                t[1]=x;
                tmap.push(t);   //添加到可移动路径
            }else break;    //如果碰到了其他棋子退出遍历
        }
    }else{
        for(var q=y+1;q<map.length&&q>=0;q++){  //黑方对帅下方各点遍历
            if(map[q][x]==0){   //如果为空点继续遍历
                continue;
            }
            if(map[q][x]==7){   //如果遇到点为对方老帅
                var t=[];
                t[0]=q;
                t[1]=x;
                tmap.push(t);   //添加到可移动路径
            }else break;    //如果碰到了其他棋子退出遍历
        }
    }
}
