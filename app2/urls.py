from django.conf.urls import patterns, url

from app2 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)