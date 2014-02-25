from django.conf.urls import *
import views
urlpatterns = patterns('',
    (r'^$',views.games))