from django.db import models
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name
    

class TutorialFile(models.Model):
    name = models.CharField(max_length=150)
    file_obj = models.FileField(upload_to="tutorial/")
    
    def __unicode__(self):
        return self.name

class TutorialSeries(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    ordinal = models.IntegerField()
    tags = models.ManyToManyField(Tag, blank=True)
    is_published = models.BooleanField()
    url_friendly_title = models.CharField(max_length=150, blank=True)
    
    def __unicode__(self):
        return self.title
    
    def get_tutorials(self, active_only=False):
        if active_only:
            qs = Tutorial.objects.filter(series=self, is_published=True)
        else:
            qs = Tutorial.objects.filter(series=self)
        return qs
    
    def save(self, *args, **kwargs):
        self.url_friendly_title = urlify(self.title)
        super(TutorialSeries, self).save(*args, **kwargs)
    

class Tutorial(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    ordinal = models.IntegerField()
    publish_date = models.DateTimeField(auto_now=True, blank=True)
    is_published = models.BooleanField()
    series = models.ForeignKey(TutorialSeries)
    files = models.ManyToManyField(TutorialFile, blank=True)
    url_friendly_title = models.CharField(max_length=150, blank=True)
    
    def __unicode__(self):
        return self.title
    
    def pages(self):
        qs = TutorialPage.objects.filter(tutorial=self)
        return qs
    
    def page(self, page_num):
        tut_page = TutorialPage.objects.get(tutorial=self, ordinal=page_num)
        return tut_page
    
    def save(self, *args, **kwargs):
        self.url_friendly_title = urlify(self.title)
        super(Tutorial, self).save(*args, **kwargs)

class TutorialPage(models.Model):
    title = models.CharField(max_length=150, blank=True)
    body = models.TextField()
    tutorial = models.ForeignKey(Tutorial)
    ordinal = models.IntegerField()
    
    def __unicode__(self):
        return str(self.ordinal) + ": " + str(self.title)


    
def urlify(text):
    to_underscore = [" ", "-"]
    to_nothing = [".", ",", "\"", "'", "(", ")"]
    for c in to_underscore:
        text = text.replace(c, "_")
    for c in to_nothing:
        text = text.replace(c, "")
    return text
    
class TutorialSeriesAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "ordinal",)
    
class TutorialAdmin(admin.ModelAdmin):
    list_display = ("title", "series", "is_published", "ordinal",)
    
class TutorialPageAdmin(admin.ModelAdmin):
    list_display = ("ordinal", "title", "tutorial",)
    
class TutorialFileAdmin(admin.ModelAdmin):
    list_display = ("name", )
    
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    
try:
    admin.site.register(TutorialSeries, TutorialSeriesAdmin)
except AlreadyRegistered:
    pass
try:
    admin.site.register(Tutorial, TutorialAdmin)
except AlreadyRegistered:
    pass
try:
    admin.site.register(TutorialPage, TutorialPageAdmin)
except AlreadyRegistered:
    pass
try:
    admin.site.register(TutorialFile, TutorialFileAdmin)
except AlreadyRegistered:
    pass
try:
    admin.site.register(Tag, TagAdmin)
except AlreadyRegistered:
    pass