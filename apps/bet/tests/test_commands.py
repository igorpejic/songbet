from django.test import TestCase

from model_mommy import mommy

from apps.bet.models import *  # noqa
from apps.bet.management.commands import check_if_won


class CheckIfWonTestCase(TestCase):
    fixtures = ['fixture1.json']

    def test_fixtures_loaded(self):
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(Better.objects.all().count(), 1)

    def test_winning_bet(self):
        bet = mommy.make(Bet, better=Better.objects.all()[0], has_won='Pending',
                         bet_type='3', stake=10.0, week=Week.objects.get(id=1))
        mommy.make(BetItem, bet=bet, song=Song.objects.get(id=1), choice='X', odd=2.0)
        mommy.make(BetItem, bet=bet, song=Song.objects.get(id=2), choice='2', odd=2.0)
        check_if_won.check_if_won(Week.objects.get(id=1), Week.objects.get(id=2))

        self.assertEqual(Better.objects.all()[0].points, 140)

    def test_losing_bet(self):
        bet = mommy.make(Bet, better=Better.objects.all()[0], has_won='Pending',
                         bet_type='3', stake=10.0, week=Week.objects.get(id=1))
        mommy.make(BetItem, bet=bet, song=Song.objects.get(id=1), choice='1', odd=2.0)

        check_if_won.check_if_won(Week.objects.get(id=1), Week.objects.get(id=2))

        self.assertEqual(Better.objects.all()[0].points, 100)

    def test_losing_bet_with_one_winning_bet_item(self):
        bet = mommy.make(Bet, better=Better.objects.all()[0], has_won='Pending',
                         bet_type='3', stake=10.0, week=Week.objects.get(id=1))
        mommy.make(BetItem, bet=bet, song=Song.objects.get(id=1), choice='X', odd=2.0)
        mommy.make(BetItem, bet=bet, song=Song.objects.get(id=2), choice='1', odd=2.0)

        check_if_won.check_if_won(Week.objects.get(id=1), Week.objects.get(id=2))

        self.assertEqual(Better.objects.all()[0].points, 100)
