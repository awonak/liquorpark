from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^gift-card$', views.gift_card, name='gift_card'),
    url(r'^gift-card-payment$', views.gift_card_payment, name='gift_card_payment'),
    url(r'^clover/margincalc$', views.margincalc, name='margincalc'),
]
