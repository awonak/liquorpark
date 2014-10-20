from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^$', 'app.views.index', name='index'),
    url(r'^about$', 'app.views.about', name='index'),
    url(r'^proprietors$', 'app.views.proprietors', name='proprietors'),
    url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^contact/thanks$', 'app.views.contact_thanks', name='contact-thanks'),


    #url(r'^admin/', include(admin.site.urls)),
)
