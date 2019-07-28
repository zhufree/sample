from django.shortcuts import render, Http404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Restaurant

import json
import random
# Create your views here.

def index(request):
    if request.user.is_authenticated():
        rests = request.user.like_restaurant.all()
        return render(request, 'eat_index.html', {'rests': rests})
    else:
        return HttpResponseRedirect('/accounts/login/')


def add_rest(request):
    if request.method == 'POST':
        new_rest = Restaurant.objects.create(
            name=request.POST.get('restname'),
            count=0,
            user=request.user
        )
        new_rest.save()
        request.user.like_restaurant.add(new_rest)
        data = {
            'name': new_rest.name,
            'count': 0,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        raise Http404


def roll(request):
    if request.method == 'POST':
        rests = request.user.like_restaurant.all()
        result = random.choice(rests)
        print(result)
        data = {
            'result': result.name,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        raise Http404