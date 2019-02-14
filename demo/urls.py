from django.conf.urls import url

from . import views

app_name = 'demo'

urlpatterns= [
    url(r'^index/$', views.index, name="index"),

    url(r'^dynamic/$', views.dynamic, name="dynamic"),
    url(r'^books/$', views.book_list, name='booklist'),
    url(r'^books/create/$', views.book_create, name='book_create'),
    url(r'^books/(?P<pk>\d+)/update/$', views.book_update, name='book_update'),
    url(r'^books/(?P<pk>\d+)/delete/$', views.book_delete, name='book_delete'),

]
