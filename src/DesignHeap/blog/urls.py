from django.conf.urls.defaults import url, patterns
# from django.views.generic.list_detail import object_list  # deprecated
from DesignHeap.blog.models import Blog
from DesignHeap.blog.views import blog_list, blog_view, blog_post_view

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MyDjangoApp.views.home', name='home'),
    #url(r'^$', archive),
    url(r'^$', blog_list),
    url(r'^(?P<blog_name>\w+)/$', blog_view),
    url(r'^(?P<blog_name>\w+)/(?P<blog_post_name>\w+)/$', blog_post_view),
    )
