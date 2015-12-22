import logging
from apps.bet.models import Bet, Week, Position

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


def check_if_won(last_week, this_week):
    assert last_week, this_week

    position_set_last_week = Position.objects.filter(week=last_week)
    position_set_this_week = Position.objects.filter(week=this_week)

    for bet in Bet.objects.filter(week=last_week):
        odds_total = 0
        if (bet.has_won != 'Pending'):
            continue
        bet.has_won = 'True'
        for betItem in bet.betitem_set.all():
            position_item_this_week = get_song_position(betItem.song, position_set_this_week)
            position_item_last_week = get_song_position(betItem.song, position_set_last_week)
	    if not position_item_this_week:
		correct_choice = '2'
	    else:
		    correct_choice = check_single_song(position_item_last_week.position,
				    position_item_this_week.position)
            odds_total += betItem.odd
            if betItem.choice != correct_choice:
                logger.info("not a god bet {} {} {}".format(bet.date_time,
                                                            betItem.song, betItem.choice))
                bet.has_won = 'False'
            else:
                logger.info("good bet {} {} {}".format(bet.date_time, betItem.song, betItem.choice))
            betItem.correct_choice = correct_choice
            betItem.save()

        bet.save()
        if bet.has_won == 'True':
            winning_points = bet.stake*odds_total
            better = bet.better
            better.points += winning_points
            better.save()


def check_single_song(song_position_last_week, song_position_this_week):
    '''returns corresponding bet choices based on changes between last week
    and this week songs position
    '''
    # Song fell off the chart
    if not song_position_this_week:
        return '2'

    if song_position_last_week > song_position_this_week:
        return '1'
    elif song_position_last_week == song_position_this_week:
        return 'X'
    else:
        return '2'


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
        parser.add_argument('week', nargs='+', type=Week)

    def handle(self, *args, **options):
        check_if_won(args[0], args[1])
