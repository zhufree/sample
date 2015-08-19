from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from blog.models import *
import markdown
# Create your views here.


def index(request):
    articles = Article.objects.all().order_by('-id')
    # for article in articles:
    #    article.content = markdown.markdown(article.content, extensions=['markdown.extensions.fenced_code'])
    return render_to_response('blogindex.html', RequestContext(request, {'articles': articles}))


def single_blog(request, id):
    cur_article = get_object_or_404(Article, pk=id)
    return render_to_response('single_article.html', RequestContext(request, {'article': cur_article}))


def tag_blogs(request, id):
    cur_tag = get_object_or_404(Tag, pk=id)
    articles = cur_tag.has_articles.all().order_by('-id')
    return render_to_response('tag_articles.html', RequestContext(request, {
        'articles': articles,
        'tag': cur_tag,
    }))
