import xmltodict
import urllib2
from json_functions import json_response
from models import Book,Shelf,Shelved,QueuedBook
from django.http import HttpResponse
from django.shortcuts import render


key = 'KMi0fKJU9NYgHcb9vMGA7A'

def books(request):
    suggestions = ["fantasy",
                   "science-fiction",
                   "40k",
                   "popular-science",
                   "science",
                   "technology",
                   "programming",
                   "computer-science",
                   "non-fiction"]
    return render(request,'books.html',{'suggestions':suggestions})

def book_json(request, bookid):
    book = get_book(bookid)
    return json_response(request,book.dict)


def get_book(bookid):
    book,created = Book.objects.get_or_create(goodreads_id=bookid)
    if created:
        url = 'https://www.goodreads.com/book/show/%s?format=xml&key=%s' % (bookid, key)
        s = urllib2.urlopen(url).read()
        xml = xmltodict.parse(s)['GoodreadsResponse']['book']

        book.title = xml['title']
        authors = xml['authors']['author']
        if type(authors) is list:
            author = authors[0]
        else:
            author = authors
        book.author = author['name']
        book.ratings_count = xml['work']['ratings_count']['#text']
        book.ratings_sum = xml['work']['ratings_sum']['#text']
        book.save()
        if 'popular_shelves' in xml:
            if xml['popular_shelves']:
                for xml_shelf in xml['popular_shelves']['shelf']:
                    shelf,created = Shelf.objects.get_or_create(name= xml_shelf['@name'])
                    if created:
                        shelf.save()
                    shelved,created = Shelved.objects.get_or_create(book = book,shelf=shelf)
                    shelved.shelved_times = xml_shelf['@count']
                    shelved.save()
    return book


def shelf(request,shelf_name):
    try:
        shelf = Shelf.objects.get(name=shelf_name)
        books = []
        for shelved in shelf.shelved_set.all():
            books.append({'title':shelved.book.title,
                          'author':shelved.book.author,
                          'average_rating':shelved.book.average_rating,
                          'ratings_count':shelved.book.ratings_count,
                          'score':shelved.book.ratings_sum,
                          'shelved': shelved.shelved_times,
                          'url':'https://www.goodreads.com/book/show/%s' % shelved.book.goodreads_id})
    except:
        books = []


    return render(request,'shelf.html',{'books':books,'shelf':shelf_name})

def shelf_json(request,shelf_name):
    shelf = Shelf.objects.get(name=shelf_name)
    return json_response(request,shelf.dict)


maxbooks = 1000
maxpages = maxbooks / 20

def search_shelf(request,shelf_name):
    response = HttpResponse(search_shelf_internal(shelf_name))
    response['X-Accel-Buffering'] = "no"
    return response


def search_shelf_internal(shelf_name):
    url = 'https://www.goodreads.com/search.xml?key=%s&q=%s&page=' % (key,shelf_name)
    yield "<div>Searching for %s</div>" % shelf_name
    page = 1
    totalresults = 1
    receivedresults = 0
    new_works = []
    while receivedresults < totalresults and page <= maxpages:
        s = urllib2.urlopen(url + str(page)).read()
        xml = xmltodict.parse(s)
        totalresults = int(xml['GoodreadsResponse']['search']['total-results'])
        receivedresults = int(xml['GoodreadsResponse']['search']['results-end'])
        yield "<div>Retrieved %s of %s results</div>" % (receivedresults,totalresults)
        works = xml['GoodreadsResponse']['search']['results']['work']
        for work in works:
            try:
                queuedBook = QueuedBook(goodreadsid = work['best_book']['id']['#text'])
                queuedBook.save()
            except:
                pass
        page += 1

def search_queued_books(request):
    return HttpResponse(search_queued_books_internal())

def search_queued_books_internal():
     for queuedBook in QueuedBook.objects.all():
        try:
            book = get_book(queuedBook.goodreadsid)
            yield "<div>Searched %s</div>" % book.title
            queuedBook.delete()
        except Exception as e:
            yield "<div>%s</div>" % e.message
     yield "Searched all queued Books"
