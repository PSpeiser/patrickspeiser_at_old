from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^latest_message.json$', 'Chat.chat.latest_message_json',name='latest_message.json'),
    url(r'^messages.json', 'Chat.chat.messages_json',name='messages.json'),
    url(r'^post_message','Chat.chat.post_message',name='post_message'),
    url(r'^get_new_messages.json', 'Chat.chat.get_new_messages_json',name='get_new_messages.json'),
    url(r'^$','Chat.chat.home',name='home'),
    url(r'^clear_history','Chat.chat.clear_history',name="clear_history")



)
