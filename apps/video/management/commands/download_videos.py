import traceback
import os
from os.path import join
from PIL import Image, ImageDraw, ImageFont
from pytube import YouTube
from pytube.exceptions import AgeRestricted

from django.core.management.base import BaseCommand
from apps.bet.models import *

from django.conf import settings

from apps.bet.models import Week, Position


def download_videos(test=True):
    manually_download = []
    positions = Week.objects.all()[0].position_set.all()
    songs = [p.song for p in positions][4:]
    for song in songs:
        if song.youtube_link:
            print 'Downloading video: {}'.format(song)
            link = 'http://www.youtube.com/watch?v=' + song.youtube_link
            try:
                yt = YouTube(link)
            except AgeRestricted:
                manually_download.append(link)
                continue
            try:
                video = yt.get('mp4', '720p')
                print video.filename
            except Exception:
                traceback.print_exc()
                print '\n No 720p, downloading 360p'
                video = yt.get('mp4', '360p')

            if not os.path.exists(os.path.abspath(os.path.join(settings.RAW_VIDEOS, video.filename + ".mp4"))):
                video.download(settings.RAW_VIDEOS)

    print manually_download


class Command(BaseCommand):

    def handle(self, *args, **options):
        download_videos()
