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
    url(r'^book/(.*).json','BookSearcher.booksearcher.book_json'),
    url(r'^shelf/(.*).json','BookSearcher.booksearcher.shelf_json'),
    url(r'^shelf/(.*)','BookSearcher.booksearcher.shelf'),
    url(r'^search_genre/(.*)','BookSearcher.booksearcher.search_genre'),



)
