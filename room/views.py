# -*-coding:utf-8-*-
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext 
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import json
from reserv import *

test=reservlib()#实例化

def index(request):
    return render(request, "room_index.html")

@csrf_exempt 
def check(request):
    if request.method=='POST':
        year = request.POST.get('year')  
        month = request.POST.get('month')  
        day=request.POST.get('day')
        region=request.POST.get('region')
        request.session['year']=year
        request.session['month']=month
        request.session['day']=day
        roominfo=test.getroominfo(year,month,day,region)
        if roominfo.has_key("error_code"):
            data={"success":"false","info":roominfo}     
        else:
            data={"success":"true","info":roominfo} 
    else:
        errorinfo="method error"
        data={"success":"false","info":errorinfo} 
    return HttpResponse(json.dumps(data, ensure_ascii=False),content_type='application/json')

@csrf_exempt 
def login(request):
    if request.method=='POST':
        sid=request.POST.get('sid')
        pwd=request.POST.get('pwd') 
        test.cookie=test.getcookie(sid,pwd)  
        test.getuserinfo() 
        request.session['cookie']=test.cookie
        request.session['sid']=sid
        request.session['pwd']=pwd
        if "PDS_HANDLE" in test.cookie:
            data={"success":"true"}
        else:
            data={"success":"false","info":test.cookie}
    else:
        errorinfo="method error"
        data={"success":"false","info":errorinfo} 
    return HttpResponse(json.dumps(data, ensure_ascii=False),content_type='application/json')
@csrf_exempt 
def reserv(request):
    if request.method=='POST':
        room=request.POST.get('room')
        time=request.POST.get('time')
        tel=request.POST.get('tel',"")
        email=request.POST.get('email',"aaa")
        description=request.POST.get('description',"")
        test.year=request.session.get('year')
        test.month=request.session.get('month')
        test.day=request.session.get('day')
        test.cookie=request.session.get('cookie')
        test.sid=request.session.get('sid')
        test.pwd=request.session.get('pwd')
        test.getuserinfo()   
        resultinfo=test.reservbyroom(room,time,tel,email,description)
        if type(resultinfo)==int:
            test.roomid=resultinfo
            request.session['roomid']=test.roomid
            data={"success":"true","info":resultinfo}
        else:
            data={"success":"false","info":resultinfo}
    else:
        errorinfo="method error"
        data={"success":"false","info":errorinfo} 
    return HttpResponse(json.dumps(data, ensure_ascii=False),content_type='application/json')

@csrf_exempt
def cancel(request):
    if request.method=='POST':
        test.cookie=request.session.get('cookie')
        test.roomid=request.session.get('roomid')
        cancelinfo=test.cancel()
        if type(cancelinfo)==int:
            request.session['roomid']=None
            data={"success":"true","info":cancelinfo}
        else:
            data={"success":"false","info":cancelinfo}
    else:
        errorinfo="method error"
        data={"success":"false","info":errorinfo} 
    return HttpResponse(json.dumps(data, ensure_ascii=False),content_type='application/json')

@csrf_exempt
def roomid(request):
    if request.session.get('roomid'):
        test.roomid=request.session.get('roomid')
        data={"success":"true","info":test.roomid}
    else:
        data={"success":"false","info":"no room"}
    return HttpResponse(json.dumps(data, ensure_ascii=False),content_type='application/json')

