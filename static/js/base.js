$(window).scroll(function(){
  //鼠标向下滚动时，隐藏导航栏,回到顶部时显示导航栏
  if($(this).scrollTop() > 0){
    $('nav').slideUp('slow');
  }else {
    $('nav').slideDown('slow');
  }
});
