function cause_reply(obj){
    if($("#reply_id").length>0){
        $("#reply_id").remove();
        $("textarea").empty();
    }
    var new_inp=document.createElement("input");
    var reply_floor=$(obj).next().text().substr(0,1);
    var quote_reply_content=$(obj).parent().prev().text();
    new_inp.setAttribute("type", "hidden");
    new_inp.setAttribute("id", "reply_id");
    new_inp.setAttribute("name", "reply_id");
    new_inp.setAttribute("value", reply_floor);
    $('#post_field').append(new_inp);
    $("textarea").append("回复"+reply_floor+"楼：<br>"+quote_reply_content+"<br>");
}
