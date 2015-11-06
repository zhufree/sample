# Create your views here.
from django.http import HttpResponse,Http404
import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from library import *
from usersys.models import StudentAcc


@login_required
def index(request):
    accounts = request.user.has_student_account.all()
    return render(request, "book_index.html", {'accounts': accounts})


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
        lib_cookie = getcookie(sid, pwd)
        request.session['_lib_cookie'] = lib_cookie
        if "PDS_HANDLE" in lib_cookie:
            data = {"status": True, "sid": sid}
        else:
            data = {"status": False, "info": lib_cookie}
    else:
        raise Http404
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_protect
def login(request):
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        cur_stuacc = StudentAcc.objects.get(sid=stu_id)
        lib_cookie = getcookie(cur_stuacc.sid, cur_stuacc.pwd)
        request.session['_lib_cookie'] = lib_cookie
        if "PDS_HANDLE" in lib_cookie:
            data = {"status": True}
        else:
            data = {"status": False, "info": lib_cookie}
    else:
        raise Http404
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_exempt
def historybook(request):
    if request.method == 'POST':
        lib_cookie = request.session.get('_lib_cookie')
        info = queryhistory(lib_cookie)
        if type(info) == list:
            data = {"status": True, "info": info}
        else:
            data = {"status": False, "info": info}

    else:
        raise Http404
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_exempt
def nowbook(request):
    if request.method == 'POST':
        lib_cookie = request.session.get('_lib_cookie')
        info = queryloan(lib_cookie)
        if type(info) == list:
            data = {"status": True, "info": info}
        elif type(info) == dict:
            data = {"status": False, "info": info}
        else:
            data = {"status": False, "info": info}
    else:
        raise Http404
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_exempt
def renewall_(request):
    if request.method == 'POST':
        lib_cookie = request.session.get('_lib_cookie')
        info = renewall(lib_cookie)
        if type(info) == str:
            data = {"status": True, "info": info}
        else:
            data = {"status": False, "info": info}
    else:
        raise Http404
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_exempt
def renew_(request):
    if request.method == 'POST':
        lib_cookie = request.session.get('_lib_cookie')
        number = int(request.POST.get('number'))
        info = renew(lib_cookie, number)
        if type(info) == str:
            data = {"status": True, "info": info}
        else:
            data = {"status": False, "info": info}
    else:
        raise Http404
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_exempt
def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        lib_cookie = request.session.get('_lib_cookie')
        info = searchbook(lib_cookie, keyword)
        if type(info) == list:
            request.session['_books_info'] = info
            data = {"status": True, "info": info}
        else:
            data = {"status": False, "info": info}
    else:
        raise Http404
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_exempt
def order(request):
    if request.method == 'POST':
        num = request.POST.get('num', '')
        lib_cookie = request.session.get('_lib_cookie')
        books_info = request.session.get('_books_info')
        book_to_order = None
        for book in books_info:
            if book['BookNum'] == num:
                book_to_order = book
        if book_to_order:
            info = orderbook(lib_cookie, book_to_order)
            if info == 'order succeed':
                data = {"status": True, "info": info}
            else:
                data = {"status": False, "info": info}
        else:
            data = {"status": False, "info": 'no such book'}
    else:
        raise Http404
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_exempt
def queryorder_(request):
    if request.method == 'POST':
        lib_cookie = request.session.get('_lib_cookie')
        info = queryorder(lib_cookie)
        if type(info) == list:
            request.session['orders'] = info
            data = {"status": True, "info": info}
        else:
            data = {"status": False, "info": info}
    else:
        raise Http404
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_exempt
def deleteorder_(request):
    if request.method == 'POST':
        lib_cookie = request.session.get('_lib_cookie')
        num = request.POST.get('num', '')
        orders = request.session['orders']
        order_to_delete = None
        for order in orders:
            if order['BookNum'] == num:
                order_to_delete = order
        if order_to_delete:
            info = deleteorder(lib_cookie, order_to_delete)
            if info == 'cancel succeed':
                data = {"status": True, "info": info}
            else:
                data = {"status": False, "info": info}
        else:
            data = {"status": False, "info": 'no such order'}
    else:
        raise Http404
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')

