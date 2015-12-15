from os.path import join
from PIL import Image, ImageDraw, ImageFont
from apps.bet.models import *
from matplotlib import pyplot as plt
import matplotlib
from numpy import linspace
import numpy as np
from fractions import Fraction

from django.conf import settings

from apps.bet.models import Week, Position

from django.core.management.base import BaseCommand


def draw_text_with_border(object, coord, text, font, multiline_text=False):
    shadowcolor = (0, 0, 0, 255)
    x, y = coord
    method = 'multiline_text' if multiline_text else 'text'
    getattr(object, method)((x-1, y-1), text, font=font, fill=shadowcolor)
    getattr(object, method)((x+1, y-1), text, font=font, fill=shadowcolor)
    getattr(object, method)((x-1, y+1), text, font=font, fill=shadowcolor)
    getattr(object, method)((x+1, y+1), text, font=font, fill=shadowcolor)
    getattr(object, method)((x, y), text, font=font, fill=(255, 255, 255, 255))


def generate_images(test_mode=True):

    base = Image.open(join(settings.IMAGE_ASSETS, 'lower_third.png')).convert('RGBA')
    up = Image.open(join(settings.IMAGE_ASSETS, 'up.png')).convert('RGBA').resize((130, 130))
    down = Image.open(join(settings.IMAGE_ASSETS, 'down.png')).convert('RGBA').resize((130, 130))
    middle = Image.open(join(settings.IMAGE_ASSETS, 'middle.png')).convert('RGBA').resize((130, 130))
    new = Image.open(join(settings.IMAGE_ASSETS, 'new.png')).convert('RGBA').resize((130, 130))

    font = {'weight': 'bold', 'size': 14}
    matplotlib.rc('font', **font)
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['axes.linewidth'] = 2

    for position in Week.objects.all()[0].position_set.all():
        if position.position > 10 and test_mode:
            return

        # make a blank image for the text, initialized to transparent text color
        song_position = Image.new('RGBA', base.size, (0, 0, 0, 0))
        txt = Image.new('RGBA', base.size, (0, 0, 0, 0))
        weeks_on = Image.new('RGBA', base.size, (0, 0, 0, 0))
        peak = Image.new('RGBA', base.size, (0, 0, 0, 0))

        d = ImageDraw.Draw(txt)
        s = ImageDraw.Draw(song_position)
        w = ImageDraw.Draw(weeks_on)
        p = ImageDraw.Draw(peak)
        o1 =ImageDraw.Draw(peak)
        o2 =ImageDraw.Draw(peak)
        ox =ImageDraw.Draw(peak)
        font_name = join(settings.IMAGE_ASSETS, 'Bauhaus_.ttf')

        song_name = position.song.name
        song_font = 70
        font = ImageFont.truetype(font_name, song_font)
        x, y = 340, 890
        draw_text_with_border(d, (x, y), song_name, font)

        artist_name = position.song.artist.name
        artist_font = 70
        artist_font = ImageFont.truetype(font_name, artist_font)
        draw_text_with_border(d, (340, 960), artist_name, artist_font, multiline_text=True)

        if position.position < 10:
            left_margin = 55
        elif position.position == 100:
            left_margin = 10
        else:
            left_margin = 35
        font = ImageFont.truetype(font_name, 100)
        draw_text_with_border(s, (left_margin, 905), str(position.position), font)

        out = Image.alpha_composite(song_position, txt)
        assert position.change
        if position.change == '1':
            out.paste(up, (165, 885), up)
        elif position.change == '2':
            out.paste(down, (165, 885), down)
        elif position.change == 'N':
            out.paste(new, (165, 885), new)
        elif position.change == 'X':
            out.paste(middle, (165, 885), middle)

        weeks_on_n = Position.objects.filter(song=position.song).count()
        font = ImageFont.truetype(font_name, 60)
        draw_text_with_border(w, (1480, 70), "Weeks on - {}".format(weeks_on_n), font)
        out = Image.alpha_composite(out, weeks_on)

        peak_n = Position.objects.filter(song=position.song).order_by('position')[0].position
        draw_text_with_border(p, (1480, 20), "Peak - {}".format(peak_n), font)

        draw_text_with_border(p, (30, 20), "Next week odds:", font)

        odd_up = Image.open(join(settings.IMAGE_ASSETS, 'up.png')).convert('RGBA').resize((70, 70))
        odd_middle = Image.open(join(settings.IMAGE_ASSETS, 'middle.png')).convert('RGBA').resize((70, 70))
        odd_down = Image.open(join(settings.IMAGE_ASSETS, 'down.png')).convert('RGBA').resize((70, 70))

        up_margin = 95
        up_image_margin = 80
        for attr, image in [('odd_1', odd_up), ('odd_x', odd_middle), ('odd_2', odd_down)]:
            attr_n = getattr(position, attr)
            draw_text_with_border(
                p, (120, up_margin),
                "{}".format(attr_n), font=font)

            draw_text_with_border(
                p, (270, up_margin), "{}".format(Fraction(attr_n-1).limit_denominator(1000)),
                font=font)
            draw_text_with_border(
                p, (500, up_margin),
                "{:.0f}".format((attr_n - 1)*100 if attr_n >= 2 else (-100)/(attr_n-1)),
                font=font)
            out.paste(image, (30, up_image_margin), image)
            out = Image.alpha_composite(out, peak)
            up_margin += 80
            up_image_margin += 80

        outa = out.resize((1280, 720), Image.ANTIALIAS)
        outa.save(join(settings.IMAGES, "lower{}.png".format(position.position)), "PNG")

        positions = Position.objects.filter(song=position.song).order_by('week__date').values_list('position', flat=True)
        positions = list(positions)[-12:]
        positions = positions[::-1]

        # x = np.arange(1, 11)
        y = [1, 25, 50, 75, 100]
        #xs = [str(i) for  i in x]
        ys = [str(i) for i in y]

        fig, ax = plt.subplots(linewidth=20)
        #plt.xticks(x,xs)
        plt.yticks(y, ys)

        ax.set_xlim([-0.1, 10.1])
        ax.set_ylim([0, 100])
        color = 'white'
        ax.spines['left'].set_color(color)
        ax.spines['bottom'].set_color(color)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='x', colors=color)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='y', colors=color)
        plt.xlabel('LAST 10 WEEKS', fontsize=14, weight='bold', color=color)
        plt.ylabel('POSITIONS', fontsize=14, weight='bold', color=color)
        ax.margins(.95)
        for x, y in enumerate(positions):
            if x == 10:
                ax.annotate('{}'.format(y), xy=(x, y), xytext=(x, y-3), color=color, fontsize=14)
            else:
                ax.annotate('{}'.format(y), xy=(x, y), xytext=(x+0.3, y-3), color=color, fontsize=14)

        plt.gca().invert_yaxis()
        plt.gca().invert_xaxis()
        ax.plot(positions, marker='o', color='w', markersize=10)
        plt.savefig(join(settings.IMAGES, 'graph{}.png'.format(position.position)),
                    transparent=True, dpi=50)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--prod',
                            action='store_true',
                            dest='prod',
                            default=False,
                            help='Production')

    def handle(self, *args, **options):
        if options['prod']:
            generate_images(test_mode=False)
        else:
            generate_images()
