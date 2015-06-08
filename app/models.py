from django.db import models


class Article(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    url = models.URLField(unique=True)

    def __unicode__(self):
        return self.url