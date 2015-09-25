from django.shortcuts import render
from .models import Restaurant
# Create your views here.

def index(request):
    rest = request.user.like_restaurant.all()
    return render(request, 'index.html', {'rest': rest})


def add_rest(request):
    pass
