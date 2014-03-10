from django.conf.urls import patterns, url
urlpatterns = patterns('',
    url(r'^$','tweetrss.tweetrss.home',name='tweetrss_home'),
    url(r'^(.*)','tweetrss.tweetrss.rssfeed',name='tweetrss_feed'),
)

