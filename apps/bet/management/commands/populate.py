import time
from datetime import datetime
from datetime import date
from datetime import timedelta
import re

import urllib

from bs4 import BeautifulSoup
from apps.bet.models import Week, Song, Position, Artist

from django.core.management.base import BaseCommand

from apps.bet.management.commands import check_if_won


class WeeklyChart(object):

    def __init__(self, url, checked, check_won=False):
        self.url = url
        self.checked = checked

        sock = urllib.urlopen(url)
        htmlSource = sock.read()
        sock.close()
        soup = BeautifulSoup(htmlSource)
        song_name = []
        artist_names = []
        chart = []
        artists = []
        for node in soup.select(".row-title > h2"):
            song_name.append(''.join(node.findAll(text=True)).strip())
        for node in soup.select(".row-title > h3"):
            artist = ''.join(node.findAll(text=True)).strip()
            artist_names.append(artist)
            if re.findall('(.*)Featuring', artist):
                artist = re.findall('(.*)Featuring', artist)[0]
            if re.findall('(.*)With', artist):
                artist = re.findall('(.*)With', artist)[0]
            artist = artist.split('&')[0]
            artist = artist.rstrip()
            artists.append(artist)

        chart = zip(song_name, artists, artist_names)

        week_time = time.strptime(soup.time.text, "%B %d, %Y")
        dt = datetime.fromtimestamp((time.mktime(week_time)))
        if check_won:
            last_week = Week.objects.get(date=dt-timedelta(days=7))
        this_week = Week.objects.get_or_create(date=dt)[0]

        for position, (song_name, artist, artist_name) in enumerate(chart):
            artist = Artist.objects.get_or_create(name=artist)[0]
            song = Song.objects.get_or_create(name=song_name, artist=artist,
                                              artist_name=artist_name)[0]
            Position.objects.get_or_create(week=this_week, song=song,
                                           position=position + 1)

        if check_won and this_week != last_week and checked is False:
            check_if_won.check_if_won(last_week, this_week)


def populate(check_won=False):
    url = 'http://www.billboard.com/charts/hot-100'
    checked = False
    WeeklyChart(url, checked, check_won=check_won)
    url += '/'
    today = date.today()
    week_sunday = today + timedelta(days=-today.weekday() - 2,
                                    weeks=1)
    time_delta = timedelta(days=-7)
    checked = False
    for i in xrange(10):
        WeeklyChart(url + str(week_sunday), checked)
        week_sunday = week_sunday + time_delta
        print week_sunday


class Command(BaseCommand):

    help = '''
    Populate new week with video_id. Accepts 'check_won' as True or False.
    Usage: python manage.py populate --check_won
    '''

    def add_arguments(self, parser):
        parser.add_argument('--check_won', action='store_true', dest='check_won',
                            default=False, help='Check if won for last week.')

    def handle(self, *args, **options):
        if options['check_won']:
            populate(check_won=True)
        else:
            populate()
