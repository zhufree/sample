from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from usersys.forms import *
from pyquery import PyQuery as pq
import json

spider_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/68.0.3440.106 '
                  'Safari/537.36'}


# Create your views here.

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def get_latest_article(request, page_type, page_index):
    article_list = []
    type_str = "created-cn" if page_type == 0 else "created-translated"
    # doc = pq('http://scp-wiki-cn.wikidot.com/most-recently-created-cn/p/1')
    link_str = 'http://scp-wiki-cn.wikidot.com/most-recently-%s/p/%s' % (type_str, page_index)
    doc = pq(link_str)
    for i in list(doc('table>tr').items())[2:]:
        new_article = {}
        info_list = list(i('td').items())
        new_article['title'] = info_list[0]('a').text()
        new_article['link'] = info_list[0]('a').attr('href')
        new_article['created_time'] = info_list[1]('span').text()
        new_article['rank'] = info_list[2].text()
        article_list.append(new_article)
    return HttpResponse(json.dumps({
        'results': article_list
    }), content_type="application/json")


def projects(request):
    return render(request, 'projects.html')


@csrf_protect
def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('disabled account')
        else:
            return HttpResponse('invalid login')
    return render(request, 'login.html')


def logout_(request):
    logout(request)
    return HttpResponseRedirect('/')


@csrf_protect
def register_(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            new_user.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render(request, 'register.html', variables)


@csrf_exempt
def api_login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            if user.is_active:
                login(request, user)
                data = {'status': True, 'info': 'login succeed'}
                return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')
            else:
                data = {'status': False, 'info': 'login failed'}
                return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')
        else:
            data = {'status': False, 'info': 'no such user'}
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')
    else:
        data = {'status': False, 'info': 'method error'}
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_exempt
def api_logout_(request):
    logout(request)
    data = {'status': True, 'info': 'logged out'}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')


@csrf_exempt
def api_register_(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            new_user.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            data = {'status': True, 'info': 'register succeed'}
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render(request, 'register.html', variables)
