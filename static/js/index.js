var now = new Date();
var dateStr = "现在是" +
now.getFullYear() + "年" +
now.getMonth() + 1 + "月" +
now.getDate() + "日" +
now.getHours() + ":" +
now.getMinutes() + ":" +
now.getSeconds();
console.log(dateStr);
var timeHead = $('<p id="timeHead"></p>').text(dateStr);
$('#cover').html(timeHead);
$('#cover').click(function(){
  $('#cover').hide();
})
