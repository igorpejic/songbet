import random
import math
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

duration = 3
change_image_size = position_image_size = {'x': 180, 'y': 180}
lower_third_size = {'x': 1500, 'y': 180}


def subscribers_video():

    subscriber_videos = []
    random.seed()
    with open(join(settings.VIDEO_ASSETS, "subscribers.txt")) as f:
        subscribers = f.read()
    subscribers = subscribers.split("\n")[:-1]
    background = ImageClip(join(settings.IMAGE_ASSETS,
                                "subscribers_bg.png")).set_duration(duration)
    title = TextClip(txt="SPECIAL THANKS TO OUR SUBSCRIBERS!", color='white',
                     font='gill_sans.txt', fontsize=60).set_duration(duration)
    title = title.set_pos((350, 10))
    t1 = 1
    for sub_name in subscribers:
        t1 += 0.2
        t0 = math.log(t1)
        subscriber = TextClip(txt=sub_name, color='white',
                              font='gill_sans.txt', fontsize=40).set_duration(duration)
        x, y = random.random() * 1700, random.random() * 940 + 100
        subscriber = subscriber.set_pos(lambda t, t0=t0, x=x, y=y: (
            (x, (y, -200)[t < t0])))
        subscriber_videos.append(subscriber)

    audioclip = VideoFileClip(join(settings.VIDEO_ASSETS, "gunfire.mp4"))

    final = CompositeVideoClip([audioclip, background, title] + subscriber_videos, size=((1920, 1080))).fadeout(0.2)
    return final
