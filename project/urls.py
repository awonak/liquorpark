from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app.views.index', name='index'),
    url(r'^about$', 'app.views.about', name='index'),
    url(r'^proprietors$', 'app.views.proprietors', name='proprietors'),
    url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^contact/thanks$', 'app.views.contact_thanks', name='contact-thanks'),
    url(r'^events$', 'app.views.events', name='events'),
    url(r'^press$', 'app.views.press', name='press'),

    url(r'^clover/margincalc$', 'app.views.margincalc', name='margincalc'),

    url(r'^a/', include(admin.site.urls)),
)
