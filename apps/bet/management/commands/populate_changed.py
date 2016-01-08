from apps.bet.models import Week

from django.core.management.base import BaseCommand


def populate_change(all=True):
    if all:
        i = 0
        weeks = Week.objects.all().order_by('date')
        for week in range(len(weeks) - 1):
            print week
            previous_week = weeks[i]
            week = weeks[i+1]
            sync_change(week, previous_week)
            i += 1
    else:
        week = Week.objects.all().order_by('-date')[0]
        previous_week = Week.objects.all().order_by('-date')[1]
        sync_change(week, previous_week)


def sync_change(week, previous_week):
    for position in week.position_set.all():
        last_week_position = get_song_position(position.song, previous_week.position_set.all())
        if not last_week_position:
            position.change = 'N'
        else:
            position.change, position.n_change = check_single_song(last_week_position.position,
                                                                   position.position)
        position.save()


def check_single_song(song_position_last_week, song_position_this_week):
    '''returns corresponding bet choices based on changes between last week
    and this week songs position
    '''
    if song_position_last_week > song_position_this_week:
        return '1', song_position_last_week - song_position_this_week
    elif song_position_last_week == song_position_this_week:
        return 'X', song_position_last_week - song_position_this_week
    else:
        return '2', song_position_last_week - song_position_this_week


def get_song_position(betItem_song, position_set):
    '''returns one position object which purpose is to provide position for comparison
    '''
    item = [item for item in position_set if betItem_song == item.song]
    if item:
        return item[0]
    return None


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('all', nargs='+', type=str)

    def handle(self, *args, **options):
        if options['all'][0] == 'all':
            populate_change(all=True)
        else:
            populate_change(all=False)
