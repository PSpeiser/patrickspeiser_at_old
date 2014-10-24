from django.views.decorators.cache import cache_page
from django.shortcuts import render

from datetime import date, datetime

year = date.today().year
goodPlatforms = ['Win']


@cache_page(60 * 60 * 6) #cache for 6 hours
def games(request):
    games = get_games_from_wikipedia()
    games.append({'date': datetime.now().strftime('%Y-%m-%d'),
                  'name': u'Today',
                  'platforms': 'Date'})
    games.sort(key=lambda x: x['date'])
    return render(request, 'games.html', {'games': games,
                                          'filter': goodPlatforms,
                                          'year': year})


#This gets the game releases from http://en.wikipedia.org/wiki/2014_in_video_gaming?printable=yes
#Ugly Code
def get_games_from_wikipedia():
    import urllib2

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    url = "http://en.wikipedia.org/wiki/%s_in_video_gaming?printable=yes" % year
    page = opener.open(url).read()
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(page)
    tables = soup.find_all('table')
    #find tables
    tables = [table for table in tables
              if table.get('class')
        and 'wikitable' in table.get('class')]
    #only use the tables with release dates and platforms in them
    tables = [table for table in tables
              if 'Platform(s)' in (table.findChild('tr').text)]

    games = []
    for table in tables:
        #extract rows
        rows = table.findAll('tr')
        #remove header
        rows.pop(0)
        lastDate = -1
        for row in rows:
            elements = row.findAll('td')
            gamedate = elements[-3].text if len(elements) >= 3 else lastDate
            #assign day 32 as a placeholder
            if gamedate == '' or gamedate == 'TBA':
                gamedate = '32'
            gamedate = int(gamedate)
            if len(elements) < 2:
                continue
            name = elements[-2].text
            platforms = elements[-1].text
            game = {'date': gamedate,
                    'name': name,
                    'platforms': platforms}
            games.append(game)
            lastDate = gamedate

    #add proper dates
    import calendar

    month = 1
    last_date = 0
    for game in games:
        if game['date'] < last_date:
            month += 1
        if game['date'] == 32:
            game['date'] = calendar.monthrange(year, month)[1]
        last_date = game['date']
        game['date'] = '-'.join([str(year), str(month).rjust(2, '0'), str(game['date']).rjust(2, '0')])

    games = [game for game in games if any(goodPlatform in game['platforms'] for goodPlatform in goodPlatforms)]

    return games