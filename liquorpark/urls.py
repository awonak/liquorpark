from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'promo.views.index', name='index'),
    url(r'^about$', 'promo.views.about', name='index'),
    url(r'^proprietors$', 'promo.views.proprietors', name='proprietors'),
    url(r'^contact$', 'promo.views.contact', name='contact'),
    url(r'^contact/thanks$', 'promo.views.contact_thanks', name='contact-thanks'),


    #url(r'^admin/', include(admin.site.urls)),
)
