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

        week_time = time.strptime(soup.time.text, "%B %d, %Y")
        dt = datetime.fromtimestamp((time.mktime(week_time)))
        this_week = Week.objects.get_or_create(date=dt)[0]

        for i in range(1, 101):
            article = soup.find(class_="chart-row--{}".format(i))
            article_secondary = article.find(id="chart-row-{}-secondary".format(i))
            artist_name = article.select(".chart-row__title > h3")[0].getText().strip()
            song_name = article.select(".chart-row__title > h2")[0].getText().strip()

            artist = Artist.objects.get_or_create(name=artist_name)[0]
            song = Song.objects.get_or_create(name=song_name, artist=artist,
                                              artist_name=artist_name)[0]
            position = Position.objects.get_or_create(week=this_week, song=song,
                                                      position=i)[0]

            awards = article_secondary.find(class_="chart-row__awards")
            if awards:
                for award in awards.findAll('li'):
                    performance_gain = award.find(class_="fa-dot-circle-o")
                    if performance_gain:
                        position.performance_gain = True
                        position.save()

                    airplay_gain = award.find(class_="fa-microphone")
                    if airplay_gain:
                        this_week.airplay_gain = i
                    stream_gain = award.find(class_="fa-signal")
                    if stream_gain:
                        this_week.stream_gain = i
                    digital_gain = award.find(class_="fa-usd")
                    if digital_gain:
                        this_week.digital_gain = i
                    highest_ranking_debut = award.find(class_="fa-angle-double-up")
                    if highest_ranking_debut:
                        this_week.highest_ranking_debut = i

        this_week.save()
        if check_won:
            last_week = Week.objects.all().order_by('-date')[1]

        if check_won and this_week != last_week and checked is False:
            check_if_won.check_if_won(last_week, this_week)


def populate(check_won=False):
    url = 'http://www.billboard.com/charts/hot-100'
    checked = False
    WeeklyChart(url, checked, check_won=check_won)
    url += '/'
    today = date.today()
    week_sunday = today + timedelta(days=-today.weekday() - 2,
                                    weeks=2)
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
