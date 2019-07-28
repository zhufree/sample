$(function() {
   updateMsg();    //更细信息
           //表单 submit 事件
   $("#chatForm").submit(function() {
       //ajax 提交表单
       $.post("./post/",
         $('#chatForm').serialize(),
         function(data) {
           $("#content").val("");  //消息发送成功后清空内容框
           //addMsg(xml);    //处理 xml
       });
       return false;       //阻止表单提交
   });
});

//更新消息
function updateMsg() {
   $.post(
     "./post/",
     {
       post_type: "get_chat",
     last_chat_id: $(".chat_id").last().val()
   },
   function(data) {
         $('.list-group-item').append(data);    //解析返回的 xml
   });
   setTimeout(updateMsg, 1000);        //每秒更新一次
}
