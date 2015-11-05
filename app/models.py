from django.db import models

from opengraph import OpenGraph


class Article(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    url = models.URLField(unique=True)
    # derived meta fields
    site_name = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):

        # Check if we need to get the metadata
        if self.site_name == "":
            self.__dict__.update(OpenGraph(url=self.url))

        super(Article, self).save(*args, **kwargs)
