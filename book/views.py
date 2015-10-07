# Create your views here.
from django.http import HttpResponse
import json
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from library import *


def index(request):
    return render(request, "book_index.html")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        sid = request.POST.get('sid','')
        pwd = request.POST.get('pwd','')
        cookie = getcookie(sid, pwd)
        request.session['cookie_'] = cookie
        #request.session['sid'] = sid
        #request.session['pwd'] = pwd
        if "PDS_HANDLE" in cookie:
            data = {"success": "true"}
        else:
            data = {"success": "false", "info": cookie}
    else:
        errorinfo = "method error"
        data = {"success": "false", "info": errorinfo}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_exempt
def historybook(request):
    if request.method == 'POST':
        cookie = request.session.get('cookie_')
        info = queryhistory(cookie)
        if type(info) == list:
            data = {"success": "true", "info": info}
        else:
            data = {"success": "false", "info": info}
    else:
        errorinfo = "method error"
        data = {"success": "false", "info": errorinfo}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_exempt
def nowbook(request):
    if request.method == 'POST':
        cookie = request.session.get('cookie_')
        info = queryloan(cookie)
        if type(info) == list:
            data = {"success": "true", "info": info}
        elif type(info) == dict:
            data = {"success": "false", "info": info}
        else:
            data = {"success": "false", "info": info}
    else:
        errorinfo = "method error"
        data = {"success": "false", "info": errorinfo}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')

@csrf_exempt
def renewall_(request):
    if request.method == 'POST':
        cookie = request.session.get('cookie_')
        info = renewall(cookie)
        if type(info) == str:
            data = {"success": "true", "info": info}
        else:
            data = {"success": "false", "info": info}
    else:
        errorinfo = "method error"
        data = {"success": "false", "info": errorinfo}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')

@csrf_exempt
def renew_(request):
    if request.method == 'POST':
        cookie = request.session.get('cookie_')
        number=int(request.POST.get('number'))
        info = renew(cookie,number)
        if type(info) == str:
            data = {"success": "true", "info": info}
        else:
            data = {"success": "false", "info": info}
    else:
        errorinfo = "method error"
        data = {"success": "false", "info": errorinfo}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')

@csrf_exempt
def search(request):
    if request.method=='POST':
        keyword=request.POST.get('keyword','')
        cookie=request.session.get('cookie_')
        #print cookie
        info=searchbook(cookie,keyword)
        if type(info)==list:
            request.session['booksinfo']=info
            data= {"success": "true", "info": info}
        else:
            data={"success": "false", "info": info}
    else:
        errorinfo = "method error"
        data = {"success": "false", "info": errorinfo}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')

@csrf_exempt
def order(request):
    if request.method=='POST':
        num=request.POST.get('num','')
        cookie=request.session.get('cookie_')
        booksinfo=request.session.get('booksinfo')
        book_to_order=None
        for book in booksinfo:
            if book['Num']==num:
                book_to_order=book
        if book_to_order:

            info=orderbook(cookie,book_to_order)
            #print info
            if info=='order succeed':
                data= {"success": "true", "info": info}
            else:
                data={"success": "false", "info": info}
        else:
            data= {"success": "false", "info": 'no such book'}
        
    else:
        errorinfo = "method error"
        data = {"success": "false", "info": errorinfo}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')

@csrf_exempt
def queryorder_(request):
    if request.method=='POST': 
        cookie=request.session.get('cookie_')
        info=queryorder(cookie)
        if type(info)==list:
            request.session['orders']=info
            data= {"success": "true", "info": info}
        else:
            data={"success": "false", "info": info}
    else:
        data = {"success": "false", "info": "method error"}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')

@csrf_exempt
def deleteorder_(request):
    if request.method=='POST': 
        cookie=request.session.get('cookie_')
        num=request.POST.get('num','')
        orders=request.session['orders']
        order_to_delete=None
        for order in orders:
            if order['Num']==num:
                order_to_delete=order
        if order_to_delete:
            info=deleteorder(cookie,order_to_delete)
            if info=='cancel succeed':
                data= {"success": "true", "info": info}
            else:
                data={"success": "false", "info": info}
        else:
            data= {"success": "false", "info": 'no such order'}
    else:
        data = {"success": "false", "info": "method error"}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')

