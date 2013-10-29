from django.conf.urls import patterns, url

from app_sentence import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)