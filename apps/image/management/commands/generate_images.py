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


def draw_position(position):
    size = 180
    text = str(position)
    rectangle = Image.new('RGBA', (size, size), (0, 0, 0, 0))

    draw = ImageDraw.Draw(rectangle)
    draw.rectangle([0, 0, size, size], fill="#000000")

    font_name = join(settings.IMAGE_ASSETS, 'Bauhaus_.ttf')
    font_size = 140
    font = ImageFont.truetype(font_name, font_size)

    w, h = draw.textsize(str(text), font=font)

    draw.text(((size - w) / 2, (size-h) / 2), text, font=font)
    del draw
    rectangle.save(join(settings.IMAGES, "pos{}.png".format(position)))

def draw_change(position):
    size = 180
    rectangle = Image.new('RGBA', (size, size), (0, 0, 0, 0))

    draw = ImageDraw.Draw(rectangle)

    up = Image.open(join(settings.IMAGE_ASSETS, 'arrow-up.png')).convert('RGBA').resize((130, 130))
    down = Image.open(join(settings.IMAGE_ASSETS, 'arrow-down.png')).convert('RGBA').resize((130, 130))
    middle = Image.open(
        join(settings.IMAGE_ASSETS, 'arrow-middle.png')).convert('RGBA').resize((130, 130))
    new = Image.open(join(settings.IMAGE_ASSETS, 'new.png')).convert('RGBA').resize((130, 130))

    assert position.change
    paste_size = 130
    paste_pos = ((size - paste_size) / 2, (size - paste_size) / 2)

    font_name = join(settings.IMAGE_ASSETS, 'Bauhaus_.ttf')

    font_size = 50
    if position.n_change and abs(position.n_change) >= 10:
        font_size = 40

    if position.change == '1':
        paste_image = up
        fill_color = '#4CAF50'
        x, y = 120, 10
        if font_size == 40:
            x = 111
    elif position.change == '2':
        paste_image = down
        fill_color = '#F44336'
        x, y = 135, 137
        if font_size == 40:
            x = 118
    elif position.change == 'N':
        paste_image = new
        fill_color = '#FF6E1F'
    elif position.change == 'X':
        paste_image = middle
        fill_color = '#9E9E9E'

    font = ImageFont.truetype(font_name, font_size)
    draw.rectangle([0, 0, size, size], fill=fill_color)
    if position.change == '1' or position.change == '2':
        draw.text((x, y), "%+d" % position.n_change, font=font)

    rectangle.paste(paste_image, paste_pos, paste_image)

    del draw
    rectangle.save(join(settings.IMAGES, "change{}.png".format(position.position)))


def draw_lower_third(position):
    size = {'x': 1500, 'y': 180}
    rectangle = Image.new('RGBA', (size['x'], size['y']), (0, 0, 0, 0))

    draw = ImageDraw.Draw(rectangle)
    draw.polygon([(0, 0), (size['x'], 0), (size['x'] - 50, size['y']), (0, size['y'])],
                 fill=(0, 0, 0, 200))

    font_name = join(settings.IMAGE_ASSETS, 'gill_sans.ttf')
    font_size = 80

    artist = position.song.artist.name.upper()
    song = position.song.name.upper()
    if len(artist) > 20 or len(song) > 20:
        font_size = 60
    if len(artist) > 30 or len(song) > 30:
        font_size = 50
    if len(artist) > 40 or len(song) > 40:
        font_size = 45
    font = ImageFont.truetype(font_name, font_size)
    draw.text((50, 8), artist, font=font)
    w, h = draw.textsize(artist, font=font)

    draw.text((50, h + 28), song, font=font)

    font_size = 40
    font = ImageFont.truetype(font_name, font_size)
    weeks_on_n = Position.objects.filter(
        song=position.song).order_by('week_id').distinct('week').count()
    draw.text((1220, 8), "WEEKS ON: {}".format(weeks_on_n), font=font)

    w, h = draw.textsize("WEEKS ON:", font=font)

    peak_n = Position.objects.filter(song=position.song).order_by('-position')[0].position
    draw.text((1225, 21 + h), "BOTTOM: {}".format(peak_n), font=font)

    w, h1 = draw.textsize("PEAK:", font=font)

    peak_n = Position.objects.filter(song=position.song).order_by('position')[0].position
    draw.text((1225, 20*2 + h + h1), "PEAK: {}".format(peak_n), font=font)
    del draw
    rectangle.save(join(settings.IMAGES, "lower_third{}.png".format(position.position)))


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
        if position.position == 11 and test_mode:
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

        draw_position(position.position)
        draw_change(position)
        draw_lower_third(position)

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

        weeks_on_n = Position.objects.filter(song=position.song).order_by('week_id').distinct('week').count()
        font = ImageFont.truetype(font_name, 60)
        draw_text_with_border(w, (1480, 70), "Weeks on - {}".format(weeks_on_n), font)
        out = Image.alpha_composite(out, weeks_on)

        peak_n = Position.objects.filter(song=position.song).order_by('position')[0].position
        draw_text_with_border(p, (1480, 20), "Peak - {}".format(peak_n), font)

        '''
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
        '''
        outa = out.resize((1280, 720), Image.ANTIALIAS)
        outa.save(join(settings.IMAGES, "lower{}.png".format(position.position)), "PNG")

        positions = Position.objects.filter(song=position.song).order_by('-week__date').values_list('position', flat=True)
        positions = list(positions)[:11]
        #positions = positions[::-1]

        color = 'white'

        ####
        import matplotlib.animation as animation

        def update_line(num, data, line):
            line.set_data(data[..., :num])
            annotation = plt.annotate('{}'.format(data[1][num]), xy=(data[0][num], data[1][num]))
            return line, annotation

        fig = plt.figure()

        positions = positions[::-1]
        data = np.array([range(0, len(positions)), positions])
        l, = plt.plot([], [], 'r-')
        plt.xlim(-10, len(positions))
        plt.ylim(-10, 100)
        plt.gca().invert_yaxis()
        #plt.gca().invert_xaxis()
        line_ani = animation.FuncAnimation(fig, update_line, frames=len(positions), fargs=(data, l),
                                           interval=2000)
        # line_ani.save('lines.mp4', fps=len(positions))

        ####
        positions = positions[::-1]

        # from pylab import rcParams
        # rcParams['figure.figsize'] = 5, 4

        # x = np.arange(1, 11)
        y = [1, 25, 50, 75, 100]
        #xs = [str(i) for  i in x]
        ys = [str(i) for i in y]

        fig, ax = plt.subplots(linewidth=20)
        #plt.xticks(x,xs)
        plt.yticks(y, ys)

        ax.set_xlim([-0.3,  10.21])
        ax.set_ylim([-0.8, 100])
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
        _max, _min = None, None
        for x, y in enumerate(positions):
            if (not _min and y <= min(positions)):
                _min = True
                if x == 10:
                    ax.annotate('{}'.format(y), xy=(x, y), xytext=(x, y-3), color=color, fontsize=24)
                else:
                    ax.annotate('{}'.format(y), xy=(x, y), xytext=(x+0.3, y-3), color=color, fontsize=24)
            if (not _max and y >= max(positions)):
                _max = True
                if x == 10:
                    ax.annotate('{}'.format(y), xy=(x, y), xytext=(x, y-3), color=color, fontsize=24)
                else:
                    ax.annotate('{}'.format(y), xy=(x, y), xytext=(x+0.3, y-3), color=color, fontsize=24)


        x = np.arange(len(positions))
        plt.gca().invert_yaxis()
        plt.gca().invert_xaxis()
        ax.plot(x, positions, color='w', markersize=10)
        plt.savefig(join(settings.IMAGES, 'graph{}.png'.format(position.position)),
                    transparent=True, dpi=65)


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
