# Create your views here.
from django.shortcuts import render_to_response
from django.template import loader, Context
from django.http import HttpResponse

from DesignHeap.gallery.models import Album
from DesignHeap.blog.models import BlogPost

def index(request):
    return render_to_response("index.html")

def recent_activity(request):
    num_recs = 3
    albums = Album.objects.filter(public=True).order_by("-published")
    for al in albums:
        al.preview = al.preview()
    blog_posts = BlogPost.objects.filter(is_published=True).order_by("-published")
    for bp in blog_posts:
        bp.body = bp.preview()
        bp.url_str = bp.url()

    posts = [x for x in albums] + [y for y in blog_posts]
    posts.sort(key=lambda k: k.published, reverse=True)

    if len(posts) > num_recs:
        posts = posts[:num_recs]

    t = loader.get_template("activity/latest.html")
    c = Context({"posts": posts})

    return HttpResponse(t.render(c))