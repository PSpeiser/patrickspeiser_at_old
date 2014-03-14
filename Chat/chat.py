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
    messages = ChatMessage.objects.all().order_by('date')
    return json_response(request, [{'user': message.user,
                                   'message': message.message,
                                   'date': message.date,
                                   'id':message.pk} for message in messages])

def get_new_messages(request):
    last_message_id = request.GET.get('last_message_id',0)
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
        cm.date = datetime.datetime.now()
        cm.save()
        return json_response(request,'Success')
    else:
        return HttpResponse(request,"405 Method Not Allowed")