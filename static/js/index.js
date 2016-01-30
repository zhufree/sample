function showTime(){
    var now = new Date();
    var dateStr = "现在是" +
    now.getFullYear() + "年" +
    now.getMonth() + 1 + "月" +
    now.getDate() + "日" +
    now.getHours() + ":" +
    now.getMinutes() + ":" +
    now.getSeconds();
  // console.log(dateStr);
    $('#timeHead').text(dateStr);
}
function get_cookie(Name){
    var search = Name + "=" ;
    var returnvalue = "";
    if (document.cookie.length > 0) {
        offset = document.cookie.indexOf(search) ;
        if (offset != -1) {
            // 如果指定的cookie已经存在
            offset += search.length;
            // 长度指定到cookie值的位置
            end = document.cookie.indexOf(";", offset);
            // 判断是否还包括其他cookie值
            if (end == -1){
            //如果不包括
            end = document.cookie.length;
            //获取cookie的长度
            }
        returnvalue=unescape(document.cookie.substring(offset, end));
        //获取cookie的值
        }
    }
    return returnvalue;
}
$().ready(function(){
    if (get_cookie("popped")===""){
        //判断是否已经弹出过窗口
        $('#cover').show();
        setInterval(showTime, 1000);
        //如果没有则弹出窗口
        document.cookie="popped=yes";
        //设置cookie值
    }else{
        // setInterval(showTime, 1000);
        // $('#cover').show();
        // $('#cover').hide();
    }
    $('#exit-btn').click(function(){
      $('#cover').fadeOut(1000);
    });
});
