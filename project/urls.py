from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app.views.index', name='index'),
    url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^contact/thanks$', 'app.views.contact_thanks', name='contact-thanks'),

    url(r'^clover/margincalc$', 'app.views.margincalc', name='margincalc'),

    url(r'^a/', include(admin.site.urls)),
)
