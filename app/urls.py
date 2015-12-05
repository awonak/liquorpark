from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^clover/margincalc$', views.margincalc, name='margincalc'),
]
