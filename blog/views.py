from django.shortcuts import render_to_response, render, get_object_or_404, Http404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from blog.models import *
import json
# import markdown
# Create your views here.


def index(request):
    articles = Article.objects.all().order_by('-id')
    # for article in articles:
    #    article.content = markdown.markdown(article.content, extensions=['markdown.extensions.fenced_code'])
    return render(request, 'blog_index.html')


def single_blog(request, id):
    cur_article = get_object_or_404(Article, pk=id)
    comments=cur_article.has_comments.all().order_by('id')
    return render(request, 'single_article.html', {
        'article': cur_article,
        'comments': comments,
    })


def tag_blogs(request, id):
    cur_tag = get_object_or_404(Tag, pk=id)
    articles = cur_tag.has_articles.all().order_by('-id')
    return render(request, 'tag_articles.html', {
        'articles': articles,
        'tag': cur_tag,
    })


@csrf_protect
def post(request):
    if request.method == 'POST':
        if request.POST.get('post_type') == 'post_comment':
            new_comment = Comment.objects.create(
                email=request.POST.get('email', 'default@example.com'),
                name=request.POST.get('name', 'someone'),
                content=request.POST.get('content', ''),
                article=Article.objects.get(id=request.POST.get('article_id'))
            )
            new_comment.save()
            data = {
                'content': new_comment.content,
                'author': new_comment.name,
                'time': str(new_comment.time)[:-7]
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        raise Http404