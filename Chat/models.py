from django.db import models

class ChatMessage(models.Model):
    user = models.TextField()
    message = models.TextField()
    date = models.DateTimeField()