#!/usr/bin/env python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from BookSearcher.models import QueuedBook
from BookSearcher.booksearcher import get_book
def search_queued_books():
    print "Searching %s Books" % len(QueuedBook.objects.all())
    for queuedBook in QueuedBook.objects.all():
        book = get_book(queuedBook.goodreadsid)
        print "Searched %s" % book.title
        queuedBook.delete()
    print "Searched all queued Books"