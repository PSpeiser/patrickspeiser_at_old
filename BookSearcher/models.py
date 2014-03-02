from django.db import models

class Shelf(models.Model):
    name = models.CharField(max_length=128,unique=True)

    @property
    def dict(self):
        books = []
        for shelved in self.shelved_set.all():
            books.append((shelved.book.title,shelved.shelved_times))
        print books[0]
        books.sort(key=lambda x:x[1],reverse=True)
        print books[0]
        return {'name':self.name,
                'books':books}

    def __str__(self):
        return self.name

class Book(models.Model):
    goodreads_id = models.IntegerField(unique=True)
    title = models.TextField()
    author = models.TextField()
    ratings_count = models.IntegerField(default=0)
    ratings_sum = models.IntegerField(default=0)
    shelves = models.ManyToManyField(Shelf,through='Shelved')

    def __str__(self):
        return self.title

    @property
    def dict(self):
        shelves = {}
        for shelved in self.shelved_set.all():
            shelves[shelved.shelf.name] = shelved.shelved_times
        return {'goodreads_id':self.goodreads_id,
                'title':self.title,
                'author':self.author,
                'ratings_count':self.ratings_count,
                'ratings_sum':self.ratings_sum,
                'shelves':shelves,
                }
    @property
    def average_rating(self):
        return float(self.ratings_sum) / self.ratings_count

class Shelved(models.Model):
    book = models.ForeignKey(Book)
    shelf = models.ForeignKey(Shelf)
    shelved_times = models.IntegerField(default=0)

