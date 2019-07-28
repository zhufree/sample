from django.shortcuts import render, Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import *
# Create your views here.


def index(request):
    topics = Topic.objects.all()
    posts = Post.objects.all().order_by('last_reply_time')
    return render(request, 'forum_index.html', {'posts': posts, 'topics': topics})


def single_post(request, id):
    cur_post = Post.objects.get(pk=id)
    replys = cur_post.post_has_replys.all()
    return render(request, 'single_post.html', {
        'post': cur_post,
        'replys': replys,
    })


def show_topic(request, id):
    cur_topic = Topic.objects.get(pk=id)
    posts = cur_topic.has_posts.all()
    return render(request, 'single_topic.html', {'topic': cur_topic, 'posts': posts})


@login_required
def post(request):
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        if post_type == 'post_post':
            new_post = Post.objects.create(
                author=request.user,
                title=request.POST.get('title'),
                content=request.POST.get('content'),
                topic=Topic.objects.get(id=request.POST.get('belong_to_topic')),
                reply_count=0,
            )
            new_post.save()
            return HttpResponseRedirect('/forum/')
        elif post_type == 'post_reply':
            cur_post = Post.objects.get(id=request.POST.get('post_id'))
            if request.POST.get('reply_id'):
                cur_reply = Reply.objects.get(id=int(request.POST.get('reply_id')) - 1)
                new_reply = Reply.objects.create(
                    author=request.user,
                    floor_num=cur_post.reply_count+2,
                    content=request.POST.get('content'),
                    to_post=cur_post,
                    to_reply=cur_reply,
                )
            else:
                new_reply = Reply.objects.create(
                    author=request.user,
                    floor_num=cur_post.reply_count+2,
                    content=request.POST.get('content'),
                    to_post=cur_post,
                )
            new_reply.save()
            cur_post.reply_count += 1
            cur_post.save()
            return HttpResponseRedirect('/forum/p/%d/' % cur_post.id)
    else:
        raise Http404
