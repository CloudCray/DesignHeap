from django.db import models
from django.contrib import admin

import re
HTML_REGEX = r'<+[A-Za-z\s"\'=/]+>'

# Create your models here.
class Tag(models.Model):
    text = models.CharField(max_length=50)

    def __unicode__(self):
        return self.text

class Blog(models.Model):
    name = models.CharField(max_length=150)
    comment = models.TextField()
    created = models.DateTimeField(auto_now=True)
    url_safe_name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.url_safe_name = str(self.name).replace(" ", "_")
        super(Blog, self).save(*args, **kwargs)

class BlogPost(models.Model):
    post_type = "blog"
    title = models.CharField(max_length=150)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField()
    published = models.DateTimeField()
    blog = models.ForeignKey(Blog)
    tags = models.ManyToManyField(Tag)
    url_safe_name = models.CharField(max_length=150, blank=True)

    def __unicode__(self):
        return self.title

    def preview(self):
        body = re.sub(HTML_REGEX, "", self.body)
        if len(body) > 200:
            return body[:150] + "..."
        else:
            return body

    def url(self):
        return "{0}/{1}".format(self.blog.url_safe_name, self.url_safe_name)

    def save(self, *args, **kwargs):
        cs = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890_"
        new_title = self.title
        for c in (".", ",", " "):
            new_title = new_title.replace(c, "_")
        new_title = new_title.replace("__", "_")
        for c in new_title:
            if not c in cs:
                new_title = new_title.replace(c, "")
        self.url_safe_name = new_title
        super(BlogPost, self).save(*args, **kwargs)

class TagAdmin(admin.ModelAdmin):
    list_display = ("text",)

class BlogAdmin(admin.ModelAdmin):
    list_display = ("name", "created")

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created")

admin.site.register(Tag, TagAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogPost, BlogPostAdmin)