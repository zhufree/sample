$(function(){
  $('.cover').mouseover(function(){
    $(this).css('opacity', '0.5');
  }).mouseout(function(){
    $(this).css('opacity', '0.9');
  });
});
