# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

import os
from PIL import Image as PImage
from DesignHeap.settings import MEDIA_ROOT

from django.core.files import File
from os.path import join as pjoin
from tempfile import *
from shutil import copyfile


# Create your models here.
class Album(models.Model):
    post_type = "album"
    title = models.CharField(max_length=60)
    public = models.BooleanField(default=False)
    published = models.DateTimeField()
    updated = models.DateTimeField()
    
    def __unicode__(self):
        return self.title
    
    def images(self):
        lst = [x.image.name for x in self.image_set.all()]
        lst = ["<a href='/media/%s'>%s</a>" % (x, x.split('/')[-1]) for x in lst]
        return ", ".join(lst)
    
    def videos(self):
        qs = Video.objects.filter(albums=self)
        return qs
    
    def items(self):
        images = Image.objects.filter(albums=self)
        for img in images:
            img.preview = img.thumbnail2(height=96)
        videos = Video.objects.filter(albums=self)
        for vid in videos:
            vid.preview = vid.embed(width=200, height=154)
        all_items = [x for x in images] + [y for y in videos]
        all_items.sort(key=lambda k: k.created, reverse=True)
        return all_items
    
    def preview(self):
        item = self.items()[0]
        return item.preview
    
    images.allow_tags = True
    
class Tag(models.Model):
    tag = models.CharField(max_length=50)
    def __unicode__(self):
        return self.tag
    
class Image(models.Model):
    title = models.CharField(max_length=60, blank=True, null=True)
    image = models.FileField(upload_to="images/")
    tags = models.ManyToManyField(Tag, blank=True)
    albums = models.ManyToManyField(Album, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=50)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True)
    thumbnail2 = models.ImageField(upload_to="images/", blank=True, null=True)
    
    def __unicode__(self):
        return self.image.name
    
    def save(self, *args, **kwargs):
        """Save image dimensions"""
        super(Image, self).save(*args, **kwargs)
        im = PImage.open(os.path.join(MEDIA_ROOT, self.image.name))
        self.width, self.height = im.size
        
        # Large thumbnail
        fn, ext = os.path.splitext(self.image.name)
        im.thumbnail((128, 128), PImage.ANTIALIAS)
        thumb2_fn = fn + "-thumb2" + ext
        tf2 = NamedTemporaryFile(delete=False)
        im.save(tf2.name, "JPEG")
        tf2.close()
        copyfile(tf2.name, pjoin(MEDIA_ROOT, thumb2_fn))
        os.remove(tf2.name)
        # self.thumbnail2.save(thumb_fn, File(open(tf2.name)), save=False)
        
        # Small thumbnail
        im.thumbnail((40, 40), PImage.ANTIALIAS)
        thumb_fn = fn + "-thumb" + ext
        tf = NamedTemporaryFile(delete=False)
        im.save(tf, "JPEG")
        tf.close()    
        copyfile(tf.name, pjoin(MEDIA_ROOT, thumb_fn))
        os.remove(tf.name)
        # self.thumbnail.save(thumb_fn, File(open(tf.name)), save=False)  
          
        super(Image, self).save(*args, **kwargs)
        
    def size(self):
        """Image size"""
        return "%s x %s" % (self.width, self.height)
    
    def tags_(self):
        lst = [str(x[1]) for x in self.tags.values_list()]
        return ", ".join(lst)
    
    def albums_(self):
        lst = [str(x[1]) for x in self.albums.values_list()]
        return ", ".join(lst)
    
    def thumbnail(self, height=40):
        return """<a href="/media/%s"><img border="0" alt="" src="/media/%s" height="{0}" /></a>""".format(str(height)) % (
                                                                    (self.image.name, self.thumbnail_url()))
        
    def thumbnail2(self, height=128):
        return """<a href="/media/%s"><img border="0" alt="" src="/media/%s" height="{0}" /></a>""".format(str(height)) % (
                                                                    (self.image.name, self.thumbnail2_url()))
        
    def thumbnail_url(self):
        fn, ext = os.path.splitext(self.image.name)
        thumb_fn = fn + "-thumb" + ext
        return thumb_fn
    
    def thumbnail2_url(self):
        fn, ext = os.path.splitext(self.image.name)
        thumb_fn = fn + "-thumb2" + ext
        return thumb_fn
    thumbnail.allow_tags = True

        
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title"]
    
class TagAdmin(admin.ModelAdmin):
    list_display = ["tag"]
    
class ImageAdmin(admin.ModelAdmin):
    # search_fields = ["title"]
    list_display = ["__unicode__", "title", "user", "rating", "size", "tags_", 
                    "albums_", "thumbnail", "created"]
    list_filter = ["tags", "albums", "user"]
    readonly_fields = ("thumbnail2",)
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
       
class Video(models.Model):
    name = models.CharField(max_length=255)
    url_safe_name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    video_url = models.CharField(max_length=255, blank=True)
    albums = models.ManyToManyField(Album, blank=True)
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.name
    
    def tags_(self):
        lst = [str(x[1]) for x in self.tags.values_list()]
        return ", ".join(lst)
    
    def albums_(self):
        lst = [str(x[1]) for x in self.albums.values_list()]
        return ", ".join(lst)
    
    def save(self, *args, **kwargs):
        self.url_safe_name = str(self.name).replace(" ", "_")
        super(Video, self).save(*args, **kwargs)
        
    def embed(self, width=420, height=315):
        embed_str = '''<iframe width="{0}" 
        height="{1}" 
        src="{2}" 
        frameborder="0" allowfullscreen></iframe>
        '''
        return embed_str.format(str(width), str(height), self.video_url)

class VideoAdmin(admin.ModelAdmin):
    # search_fields = ["title"]
    list_display = ["__unicode__", "tags_", "albums_"]
    list_filter = ["tags", "albums"]
    
    
admin.site.register(Album, AlbumAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)