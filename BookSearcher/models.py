from django.db import models

class Book(models.Model):
    goodreads_id = models.IntegerField()
    title = models.TextField()
    author = models.TextField()
    ratings_count = models.IntegerField()
    ratings_sum = models.IntegerField()





