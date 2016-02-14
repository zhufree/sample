$(function(){
  $('.blog-box').fadeIn('slow');

  $("#comForm").submit(
    function(event) {
    /* Act on the event */
      $.post('/blog/post/',
      $('#comForm').serialize(),
      function(data) {
      /*optional stuff to do after success */
      $(".form-control").not('.name-input').val("");  //消息发送成功后清空内容框
      htmlstr = "<div class='panel-body'><h4>"+data.content+"</h4><h5>"+data.author+"at"+data.time+"</h5></div><hr>";
      $("#comment-box").append(htmlstr); //add new message
    });
      return false;
  });
});
