from django.shortcuts import render, Http404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from msgpad.models import *

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
        # return HttpResponseRedirect('/msg/')
        return render(request, 'ajax_result.html', {'msg': new_msg})
    else:
        raise Http404