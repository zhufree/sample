$(function(){
  $('.words').each(function(){
    $this = $(this);
    size = $this.attr('data-size');
    $this.css('font-size', size*5 + 'px');
    $this.css('left', (Math.random() + 0.1)*200 + 'px');
    $this.css('top', (Math.random()+0.1)*200 + 'px');
    $this.css('color', '#' + Math.round(Math.random()*999));
  });
  $('.words').each(function(){
    $(this).mouseover(function(){
      $(this).css('font-size', $(this).attr('data-size')*6 + 'px');
    });
    $(this).mouseout(function(){
      $(this).css('font-size', $(this).attr('data-size')*5 + 'px');
    });
  });
});
