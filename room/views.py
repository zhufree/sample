# -*-coding:utf-8-*-
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required

import json
import datetime

from reserv import *
from usersys.models import StudentAcc

test = Reservelib()
now=datetime.datetime.now()


@login_required
def index(request):
    accounts = request.user.has_student_account.all()
    return render(request, "room_index.html", {'accounts': accounts})


@csrf_protect
def bind(request):
    if request.method == 'POST':
        sid = request.POST.get('sid')
        pwd = request.POST.get('pwd')
        new_account = StudentAcc.objects.create(
            sid=sid,
            pwd=pwd,
            user=request.user
        )
        new_account.save()
        lib_cookie = test.getcookie(sid, pwd)
        request.session['_lib_cookie'] = lib_cookie
        if "PDS_HANDLE" in lib_cookie:
            data = {"status": True, "sid": sid}
        else:
            data = {"status": False, "info": lib_cookie}
    else:
        raise Http404
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_exempt
def check(request):
    if request.method == 'POST':
        year = request.POST.get('year',now.year)
        if year:
            pass
        else:
            year =now.year
        month = request.POST.get('month',now.month)
        if month:
            pass
        else:
            month =now.month
        day = request.POST.get('day')
        if day:
            pass
        else:
            day = now.day
        region = request.POST.get('region')
        request.session['year'] = year
        request.session['month'] = month
        request.session['day'] = day
        roominfo = test.getroominfo(year, month, day, region)
        if "error_code" in roominfo:
            data = {"status": False, "info": roominfo}
        else:
            data = {"status": True, "info": roominfo}
    else:
        errorinfo = "method error"
        data = {"status": False, "info": errorinfo}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_exempt 
def login(request):
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        cur_stuacc = StudentAcc.objects.get(sid=stu_id)
        lib_cookie = test.getcookie(cur_stuacc.sid, cur_stuacc.pwd)
        request.session['_lib_cookie'] = lib_cookie
        request.session['sid'] = stu_id
        if "PDS_HANDLE" in lib_cookie:
            data = {"status": True}
        else:
            data = {"status": False, "info": lib_cookie}
    else:
        raise Http404
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_exempt
def reserv(request):
    if request.method == 'POST':
        room = request.POST.get('room')
        time = request.POST.get('time')
        test.year = request.session.get('year')
        test.month = request.session.get('month')
        test.day = request.session.get('day')
        test.sid = request.session.get('sid')
        test.cookie = request.session.get('_lib_cookie')
        resultinfo = test.reservbyroom(room, time)
        if type(resultinfo) == int:
            test.roomid = resultinfo
            request.session['roomid'] = test.roomid
            data = {"status": True,"info": resultinfo}
        else:
            data = {"status": False,"info": resultinfo}
    else:
        errorinfo = "method error"
        data = {"status": False, "info": errorinfo}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_protect
def cancel(request):
    if request.method == 'POST':
        test.cookie = request.session.get('_lib_cookie')
        test.roomid = request.session.get('roomid')
        cancelinfo = test.cancel()
        if type(cancelinfo) == int:
            request.session['roomid'] = None
            data = {"status": True, "info": cancelinfo}
        else:
            data = {"status": False, "info": cancelinfo}
    else:
        errorinfo = "method error"
        data = {"status": False, "info": errorinfo}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_protect
def roomid(request):
    if request.session.get('roomid'):
        test.roomid = request.session.get('roomid')
        data = {"status": True, "info": test.roomid}
    else:
        data = {"status": False, "info": "no room"}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')
