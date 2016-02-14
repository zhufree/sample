$(function(){
  $("#msgForm").submit(function() {
      //ajax 提交表单
      if($("textarea").val().length > 0){
        $.post("./post/",
        $('#msgForm').serialize(),
        function(data) {
          // alert(data);
            $("textarea").val("");  //消息发送成功后清空内容框
            htmlstr = "<div class='list-group-item'><pre class='list-group-item-heading'>"+data.content+"</pre><p class='list-group-item-text' align='right'>——"+data.author+"</p><p class='list-group-item-text' align='right'>at "+data.time+"</p></div>";
            $(".list-group").append(htmlstr); //add new message
        });
      }else{
        $("textarea").attr("placeholder", "内容不能为空");
      }
        return false;       //阻止表单提交
    });
});
