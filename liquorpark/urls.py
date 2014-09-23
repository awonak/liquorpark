from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'promo.views.index', name='index'),
    #url(r'^admin/', include(admin.site.urls)),
)
