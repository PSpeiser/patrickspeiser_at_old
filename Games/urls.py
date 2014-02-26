from django.conf.urls import *
import games

urlpatterns = patterns('',
                       (r'^$', games.games))