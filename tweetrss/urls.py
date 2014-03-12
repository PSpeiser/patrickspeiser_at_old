from django.conf.urls import patterns, url
urlpatterns = patterns('',
    url(r'^$','tweetrss.tweetrss.home',name='home'),
    url(r'^(.*)','tweetrss.tweetrss.rssfeed',name='feed'),
)

