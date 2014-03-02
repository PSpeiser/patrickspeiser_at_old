import xmltodict
import urllib2
from json_functions import json_response
from models import Book,Shelf,Shelved
from django.http import HttpResponse
from django.shortcuts import render


key = 'KMi0fKJU9NYgHcb9vMGA7A'

def book_json(request, bookid):
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
    #Ugly
    if request is None:
        return created
    return json_response(request,book.dict)

def shelf(request,shelf_name):
    shelf = Shelf.objects.get(name=shelf_name)
    books = []
    for shelved in shelf.shelved_set.all():
            books.append({'title':shelved.book.title,
                          'author':shelved.book.author,
                          'average_rating':shelved.book.average_rating,
                          'ratings_count':shelved.book.ratings_count,
                          'score':shelved.book.ratings_sum,
                          'shelved': shelved.shelved_times})
    return render(request,'shelf.html',{'books':books})

def shelf_json(request,shelf_name):
    shelf = Shelf.objects.get(name=shelf_name)
    return json_response(request,shelf.dict)


maxbooks = 1000
maxpages = maxbooks / 20

def search_genre(request,genre):
    return HttpResponse(search_genre_internal(genre))

def search_genre_internal(genre):
    url = 'https://www.goodreads.com/search.xml?key=%s&q=%s&page=' % (key,genre)
    yield "<div>Searching for %s</div>" % genre
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
            #needs to be changed to a queue addition, not a view call
            book(None,work['best_book']['id']['#text'])
        page += 1