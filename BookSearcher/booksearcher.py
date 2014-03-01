import xmltodict
import urllib2
from json_functions import json_response
from models import Book

key = 'KMi0fKJU9NYgHcb9vMGA7A'


def add_book(request, bookid):
    url = 'https://www.goodreads.com/book/show/%s?format=xml&key=%s' % (bookid, key)
    s = urllib2.urlopen(url).read()
    xml = xmltodict.parse(s)['GoodreadsResponse']['book']
    book = Book()
    book.goodreads_id = bookid
    book.title = xml['title']
    book.author = xml['authors']['author']['name']
    book.ratings_count = xml['work']['ratings_count']['#text']
    book.ratings_sum = xml['work']['ratings_sum']['#text']
    shelves = {}
    for shelf in xml['popular_shelves']['shelf']:
        shelves[shelf['@name']] = int(shelf['@count'])
    book.save()

    return json_response(request, book)


def get_shelves(bookid, genre):
    url = 'https://www.goodreads.com/book/show/%s?format=xml&key=%s' % (bookid, key)
    s = urllib2.urlopen(url).read()
    xml = xmltodict.parse(s)
    xmlshelves = xml['GoodreadsResponse']['book']['popular_shelves']['shelf']
    shelves = {}
    for shelf in xmlshelves:
        shelves[shelf['@name']] = int(shelf['@count'])
    if genre not in shelves:
        return 0
    return shelves[genre]

