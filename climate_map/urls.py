from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^stations/$', views.all_stations, name='stations'),
    url(r'^search/$', views.search, name='search'),
    url(r'^station/$', views.station, name='station'),
    url(r'^temp/$', views.temperature_data, name='temp')
]

