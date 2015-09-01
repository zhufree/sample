from django.shortcuts import render, Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from models import Chat
# Create your views here.

def index(request):
    chats = list(Chat.objects.all())[-100:]
    return render(request, 'chatroom.html', {'chats': chats})


@csrf_exempt
def post(request):
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        if post_type == 'send_chat':
            new_chat = Chat.objects.create(
                content = request.POST.get('content'),
                sender = request.user,
            )
            new_chat.save()
            return HttpResponse()
        elif post_type == 'get_chat':
            last_chat_id = int(request.POST.get('last_chat_id'))
            #print last_chat_id
            chats = Chat.objects.filter(id__gt = last_chat_id)
            return render(request, 'chat_list.html', {'chats': chats})
    else:
        raise Http404
