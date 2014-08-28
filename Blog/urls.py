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
    url(r'^$', 'Blog.blog.home', name='home'),
    url(r'^editor$', 'Blog.blog.editor', name='editor'),
    url(r'^markdown.js$', 'Blog.blog.markdown_js', name='markdown.js'),
    url(r'^add_blog_post$', 'Blog.blog.add_blog_post', name='add_blog_post'),


)
