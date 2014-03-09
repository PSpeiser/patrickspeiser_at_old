from django.conf.urls import patterns, url
urlpatterns = patterns('',
    url(r'^(.*)','tweetrss.tweetrss.rssfeed',name='rssfeed'),
)

