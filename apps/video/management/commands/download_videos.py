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
            link = 'http://www.youtube.com/watch?v=' + song.youtube_link
            try:
                yt = YouTube(link)
                yt.set_filename("{} - {}".format(song.name, song.artist.name))
            except AgeRestricted:
                manually_download.append(link)
                print 'Song is age restricted, adding to manually_download list.'
                continue
            try:
                video_type = yt.filter('mp4')[-1]
                video = yt.get(video_type.extension, video_type.resolution)
            except Exception:
                traceback.print_exc()
                continue

            if not os.path.exists(os.path.abspath(os.path.join(settings.RAW_VIDEOS, video.filename + ".mp4"))):
                print 'Downloading video: {}'.format(song)
                video.download(settings.RAW_VIDEOS)
            else:
                print 'Video: {} already downlaoded. Skipping.'.format(song)

    print 'Manually download these songs: %s' % manually_download


class Command(BaseCommand):

    def handle(self, *args, **options):
        download_videos()
