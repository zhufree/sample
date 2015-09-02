from django.shortcuts import render, Http404, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from msgpad.models import *
import json
# Create your views here.


def index(request):
    msgs = Message.objects.all().order_by('id')
    return render(request, 'msg_index.html', {'msgs': msgs})


@login_required
@csrf_protect
def post(request):
    if request.method == 'POST':
        new_msg = Message.objects.create(
            content=request.POST.get('content'),
            author=request.user
        )
        new_msg.save()
        data = {
            'content': new_msg.content,
            'author': new_msg.author.username,
            'time': str(new_msg.time)[:-7]
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        raise Http404