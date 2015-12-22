from datetime import date
from datetime import timedelta
import random

from apps.bet.models import Week, Position

from django.core.management.base import BaseCommand


def populate_odds():
    week = Week.objects.all().order_by('-date')[0]
    random.seed()
    if not hasattr(Position.objects.filter(week=week)[0].position, 'odd_1'):
        for position in Position.objects.filter(week=week):
            position.odd_1 = int((random.uniform(1, 3) * 100) + 0.7) / 100.0
            position.odd_2 = int((random.uniform(1, 3) * 100) + 0.7) / 100.0
            position.odd_x = int((random.uniform(1, 3) * 100) + 0.7) / 100.0
            position.save()


class Command(BaseCommand):
    populate_odds()

    def handle(self, *args, **options):
        pass
