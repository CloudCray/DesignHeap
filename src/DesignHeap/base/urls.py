from django.conf.urls import url, patterns
# from django.views.generic.list_detail import object_list  # deprecated
from DesignHeap.base.views import recent_activity

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MyDjangoApp.views.home', name='home'),
    #url(r'^$', archive),
    url(r'^recent_activity/$', recent_activity),
    )
