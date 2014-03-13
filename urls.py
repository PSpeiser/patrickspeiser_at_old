from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'patrickspeiser_at.views.home', name='home'),
    # url(r'^patrickspeiser_at/', include('patrickspeiser_at.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^games','Games.games.games',name='games'),
    url(r'^$', 'Homepage.homepage.home', name='home'),
    url(r'^certificates','Homepage.homepage.certificates',name='certificates'),
    url(r'^robots.txt$','Robots.robots.robots',name='robots.txt'),
    url(r'^books/',include('BookSearcher.urls',namespace="booksearcher")),
    url(r'^tweetrss/',include('tweetrss.urls',namespace="tweetrss")),
    url(r'^blog/',include('Blog.urls',namespace="blog")),
    url(r'^chat/', include('Chat.urls',namespace="chat")),


)
