import PyRSS2Gen
import datetime
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request,'tweetrss.html')

def rssfeed(request, username):
    import twitter
    #requires an api_keys.py file with the following keys specified
    import api_keys
    api = twitter.Api(consumer_key=api_keys.consumer_key, consumer_secret=api_keys.consumer_secret,
                      access_token_key=api_keys.access_token_key,
                      access_token_secret=api_keys.access_token_secret)
    user_timeline = api.GetUserTimeline(screen_name=username)

    rss = PyRSS2Gen.RSS2(
        title=username,
        link="https://twitter.com/%s" % username,
        description='Tweets from %s' % username,
        lastBuildDate=datetime.datetime.now(),
        items=[
            PyRSS2Gen.RSSItem(
                title=s.text,
                description=make_twitter_links_clickable(s.text),
                pubDate=s.created_at,
                link= "https://twitter.com/%s/status/%s" % (username,s.id)
            )
            for s in user_timeline
        ]
    )

    return HttpResponse(rss.to_xml(),content_type="application/xml")

def make_twitter_links_clickable(text):
    import re
    return re.compile(r'(http:\/\/t\.co\/[a-zA-Z0-9]+)').sub(r'<a href="\1">\1</a>', text)