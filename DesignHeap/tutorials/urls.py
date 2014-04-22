from django.conf.urls import patterns, url
from DesignHeap.tutorials.models import TutorialSeries, Tutorial
from DesignHeap.tutorials.views import series_home, tutorial_home, tutorial_page

urlpatterns = patterns('',
    url(r'^$', series_home),
    url(r'^(?P<series_name>\w+)/$', tutorial_home),
    url(r'^(?P<series_name>\w+)/(?P<tutorial_name>\w+)/(?P<page_num>\w+)/$', tutorial_page),
    url(r'^(?P<series_name>\w+)/(?P<tutorial_name>\w+)/$', tutorial_page),
                       )