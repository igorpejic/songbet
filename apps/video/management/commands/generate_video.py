from os.path import join
from PIL import Image, ImageDraw, ImageFont
from apps.bet.models import *

from django.conf import settings

from apps.bet.models import Week, Position

from django.core.management.base import BaseCommand
from moviepy.audio.fx.all import audio_fadeout
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips


def generate_video(test=True):

    video_list = []
    for i, position in enumerate(Week.objects.all()[0].position_set.all()):
        if i == 1 and test:
            break
        if i == 40:
            break

        video = VideoFileClip(join(settings.VIDEO_ASSETS,
                                   "{} - {}.mp4".format(position.song.name,
                                                        position.song.artist)))
        video = audio_fadeout(video, 2)

        image = ImageClip(
            join(settings.IMAGES, "lower{}.png".format(position.position))
        ).set_duration(15)
        graph = (ImageClip(join(settings.IMAGES, "graph{}.png".format(position.position))).
                 set_duration(15).set_pos(('right', 'bottom')))

        final = CompositeVideoClip([video, image, graph], size=((1280, 720))).fadein(2).fadeout(2)
        video_list.append(final)

    FINAL = concatenate_videoclips(list(reversed(video_list)))
    FINAL.write_videofile(join(settings.VIDEOS, "final.mp4"), fps=24, codec='libx264')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--prod',
                            action='store_true',
                            dest='prod',
                            default=False,
                            help='Production')

    def handle(self, *args, **options):
        if options['prod']:
            generate_video(test=False)
        else:
            generate_video()
