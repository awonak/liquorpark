from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

admin.autodiscover()

urlpatterns = [
    # app
    url(r'^', include('app.urls')),

    # static
    url(r'^favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    url(r'^robots.txt', TemplateView.as_view(template_name='robots.txt',
        content_type='text/plain')),

    url(r'^.well-known/acme-challenge/frzk-hVve43zKw0NqAEEKFykVUlpbXUaPu_j05FLn8o', TemplateView.as_view(template_name='letsencrypt.txt', content_type='text/plain')),

    # admin
    url(r'^a/', include(admin.site.urls)),
]
