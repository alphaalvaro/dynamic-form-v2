from django.conf.urls import url

from . import views

app_name = 'demo'

urlpatterns= [
    url(r'^index/$', views.index, name="index"),

    url(r'^dynamic/$', views.dynamic, name="dynamic"),

]
