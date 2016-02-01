from os.path import join
from PIL import Image, ImageDraw, ImageFont
from apps.bet.models import *

from django.conf import settings

from apps.bet.models import Week, Position

from django.core.management.base import BaseCommand
from moviepy.audio.fx.all import audio_fadeout
from moviepy.editor import (
    VideoFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips,
    TextClip
)


def generate_video(test=True):

    video_list = []
    duration = 15
    for i, position in enumerate(Week.objects.all()[0].position_set.all()):
        if i == 2 and test:
            break
        if i == 50:
            break

        video = VideoFileClip(join(settings.VIDEO_ASSETS,
                                   "{} - {}.mp4".format(position.song.name,
                                                        position.song.artist)))
        # video = audio_fadeout(video, 2)

        image = ImageClip(
            join(settings.IMAGES, "lower{}.png".format(position.position))
        ).set_duration(duration)
        graph = (ImageClip(join(settings.IMAGES, "graph{}.png".format(position.position))).
                 set_duration(duration))

        graph = graph.set_pos(lambda t: (
            (max(1445, 1800 - t * 700), (5, int(20 - 400*t + 400*13.2))[t > 13.2])))

        ####
        w, h = video.size

        change_image_size = position_image_size = {'x': 180, 'y': 180}
        lower_third_size = {'x': 1500 , 'y': 180}
        position_image = ImageClip(
            join(settings.IMAGES, "pos{}.png".format(position.position))
        ).set_duration(duration)

        change_image = ImageClip(
            join(settings.IMAGES, "change{}.png".format(position.position))
        ).set_duration(duration)

        lower_third_image = ImageClip(
            join(settings.IMAGES, "lower_third{}.png".format(position.position))
        ).set_duration(duration)

        # I am *NOT* explaining the formula, understands who can/want.
        # txt_mov = txt_col.set_pos(lambda t: (max(w/30, int(w-0.5*w*t)), max(5*h/6, int(100*t))) )
        txt_mov = position_image.set_pos(
            lambda t: (min(0, -position_image_size['x'] + t * 400),
                       (1080 - 20 - position_image_size['y'],
                        int(1060 - position_image_size['y'] + 380*t - 380*13))[t > 13]))

        change_image_mov = change_image.set_pos(
            lambda t: (min(change_image_size['x'], -position_image_size['x'] + t * 700),
                       (1080 - 20 - position_image_size['y'],
                        int(1060 - position_image_size['y'] + 400*t - 400*13.2))[t > 13.2]))

        lower_third_mov = lower_third_image.set_pos(
            lambda t: (min(change_image_size['x'] + position_image_size['y'], -lower_third_size['x'] + t * 2500),
                       (1080 - 20 - lower_third_size['y'],
                        int(1060 - lower_third_size['y'] + 430*t - 430*13.4))[t > 13.4]))

        #final = CompositeVideoClip([video, image, graph, txt_mov], size=((1920, 1080))).fadeout(0.2)
        final = CompositeVideoClip([video, lower_third_mov, change_image_mov, txt_mov, graph], size=((1920, 1080))).fadeout(0.2)
        #final.preview(fps=20)
        video_list.append(final)

    FINAL = concatenate_videoclips(list(reversed(video_list)))
    FINAL.write_videofile(join(settings.VIDEOS, "billboard_top_50_this_week.mp4"),
                          fps=24, codec='libx264')


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
