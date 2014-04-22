# Create your views here.

from django.template import loader, Context
from django.http import HttpResponse
# from django.shortcuts import render, render_to_response
# from django.views.generic.list_detail import object_list, object_detail # Deprecated
from django.views.generic import FormView

from DesignHeap.blog.models import Blog, BlogPost, Tag

def blog_list(request):
    blogs = Blog.objects.all()
    t = loader.get_template("blog/blog_list.html")
    c = Context({"blogs": blogs.reverse()})
    return HttpResponse(t.render(c))

def blog_view(request, blog_name):
    blog = Blog.objects.get(url_safe_name=blog_name)
    posts = BlogPost.objects.filter(blog__exact=blog.pk).order_by("-published")
    t = loader.get_template("blog/blog_view.html")
    c = Context({"blog": blog, "posts": posts})
    return HttpResponse(t.render(c))

class BlogPostFormView(FormView):
    model = BlogPost

def blog_post_view(request, blog_name, blog_post_name):
    blog = Blog.objects.get(url_safe_name=blog_name)
    post = BlogPost.objects.get(blog__exact=blog.pk,
        url_safe_name=blog_post_name)
    post.body = post.body.replace("    ", "&nbsp;&nbsp;&nbsp;&nbsp;")
    t = loader.get_template("blog/blog_post_view.html")
    c = Context({"blog": blog, "post": post})
    return HttpResponse(t.render(c))