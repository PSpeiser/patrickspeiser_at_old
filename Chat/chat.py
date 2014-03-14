from models import ChatMessage
from django.shortcuts import render
from json_functions import json_response
from django.http import HttpResponse
import datetime

def latest_message_json(request):
    message = ChatMessage.objects.latest(field_name='date')
    return json_response(request, {'user': message.user,
                                   'message': message.message,
                                   'date': message.date,
                                   'id':message.pk})

def messages_json(request):
    messages = ChatMessage.objects.all().order_by('date')[:-5]
    return json_response(request, [{'user': message.user,
                                   'message': message.message,
                                   'date': message.date,
                                   'id':message.pk} for message in messages])

def get_new_messages_json(request):
    last_message_id = int(request.GET.get('last_message_id',0))
    min_id = ChatMessage.objects.count() - 5
    last_message_id = max(min_id,last_message_id)
    messages = ChatMessage.objects.filter(pk__gt=last_message_id)
    return json_response(request, [{'user': message.user,
                                   'message': message.message,
                                   'date': message.date,
                                   'id':message.pk} for message in messages])

def post_message(request):
    if request.method == "POST":
        cm = ChatMessage()
        cm.user = request.POST.get('user')
        cm.message = request.POST.get('message')
        if not cm.user or not cm.message:
            return HttpResponse("400 Bad Request You need to specify username and message")
        cm.date = datetime.datetime.now()
        cm.save()
        return json_response(request,'Success')
    else:
        return HttpResponse("405 Method Not Allowed")

def home(request):
    return render(request,'chat/home.html')

def clear_history(request):
    ChatMessage.objects.all().delete()
    return HttpResponse("Deleted History");