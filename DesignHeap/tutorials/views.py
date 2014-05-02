# Create your views here.

from django.template import loader, Context
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
# from django.views.generic.list_detail import object_list, object_detail  # deprecated
from django.views.generic import FormView
from DesignHeap.tutorials.models import TutorialSeries, Tutorial, TutorialPage, Tag

def series_home(request):
    series_list = TutorialSeries.objects.filter(is_published=True)
    t = loader.get_template("tutorials/series_list.html")
    c = Context({"series_list": series_list})
    return HttpResponse(t.render(c))

def tutorial_home(request, series_name):
    series = TutorialSeries.objects.get(is_published=True, url_friendly_title=series_name)
    tutorial_list = series.get_tutorials(active_only=True)
    t = loader.get_template("tutorials/tutorial_list.html")
    c = Context({"series": series, "tutorial_list": tutorial_list})
    return HttpResponse(t.render(c))
    

def tutorial_page(request, series_name, tutorial_name, page_num=0):
    page_num = int(page_num)
    series = TutorialSeries.objects.get(is_published=True, url_friendly_title=series_name)
    tutorial = Tutorial.objects.get(is_published=True, series=series, url_friendly_title=tutorial_name)
    
    page_query = TutorialPage.objects.filter(tutorial=tutorial)
    pages = list([x for x in page_query])
    pages.sort(key=lambda x: x.ordinal)
    
    page = TutorialPage.objects.get(tutorial=tutorial, ordinal=page_num)
    page.prev = None
    page.next = None
    if not pages:
        pages = []
    if not page_num == 0:
        page.prev = page_num - 1
    if not page_num == len(pages) - 1:
        page.next = page_num + 1
    t = loader.get_template("tutorials/tutorial_page.html")
    c = Context({"series": series, "tutorial": tutorial, "page": page, "pages": pages})
    return HttpResponse(t.render(c))