from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('DesignHeap.base.views',
    # Examples:
    url(r'^$', 'index'),
    url(r'^base/', include('DesignHeap.base.urls')),
    url(r'^blog/', include('DesignHeap.blog.urls')),
    url(r'^gallery/', include('DesignHeap.gallery.urls')),
    url(r'^tutorials/', include('DesignHeap.tutorials.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))