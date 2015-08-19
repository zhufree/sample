from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext 
from msgpad.models import *

# Create your views here.


@login_required
@csrf_protect
def index(request):
    if request.method == 'POST':
        new_msg = Message.objects.create(
            content=request.POST.get('content'),
            author=request.user
        )
        new_msg.save()
        return HttpResponseRedirect('/msg/')
    else:
        msgs = Message.objects.all().order_by('-time')
        return render_to_response('msgindex.html', RequestContext(request, {'msgs': msgs}))
