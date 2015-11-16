import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from model_mommy import mommy

from apps.bet.models import(
    Bet, Better, Week, Position, Song
)

from apps.bet.api import SocialAuthView

class MyBetsViewTest(APITestCase):

    def setUp(self):
        today = datetime.date.today()
        sunday = today + datetime.timedelta(days=-today.weekday() - 2, weeks=2)
        mommy.make(Week, date=sunday)

    def test_dont_return_other_user_bets(self):
        self.user = mommy.make(User)
        mommy.make(Better, user=self.user)
        self.other_user = mommy.make(User)
        mommy.make(Better, user=self.other_user)
        mommy.make(Bet, better=self.user.better)
        mommy.make(Bet, better=self.user.better)
        mommy.make(Bet, better=self.other_user.better)

        self.url = reverse('api:mybets-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class LastWeekViewSetTest(APITestCase):
    def setUp(self):
        today = datetime.date.today()
        sunday = today + datetime.timedelta(days=-today.weekday() - 2, weeks=2)
        self.song = mommy.make(Song, name='foo')
        self.last_week = mommy.make(Week, date=sunday)
        self.some_week = mommy.make(Week, date=sunday-datetime.timedelta(weeks=2))

    def test_return_only_latest_week_positions(self):
        self.user = mommy.make(User)
        mommy.make(Better, user=self.user)
        self.other_user = mommy.make(User)
        mommy.make(Better, user=self.other_user)
        self.last_week_position = mommy.make(Position, song=self.song, week=self.last_week)
        self.some_week_position = mommy.make(Position, week=self.some_week)

        self.url = reverse('api:lastweek-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.last_week.id)


class BetView(APITestCase):
    def setUp(self):
        today = datetime.date.today()
        sunday = today + datetime.timedelta(days=-today.weekday() - 2, weeks=2)
        self.song = mommy.make(Song, name='foo')
        self.last_week = mommy.make(Week, date=sunday)
        self.some_week = mommy.make(Week, date=sunday-datetime.timedelta(weeks=2))
        self.user = mommy.make(User)

    def test_user_cant_make_his_points_negative(self):
        mommy.make(Better, user=self.user, points=2)
        self.last_week_position = mommy.make(Position, song=self.song, week=self.last_week)
        self.some_week_position = mommy.make(Position, week=self.some_week)

        self.url = reverse('api:bet')
        self.client.force_authenticate(user=self.user)
        self.data = {'stake': 3, 'bet_type': 3, 'date': self.last_week.date,
                     'bets': [{'choice': 1, 'song': self.song.id}]}

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Insufficient points.'})

    def test_user_cant_bet_without_stake(self):
        mommy.make(Better, user=self.user, points=2)
        self.last_week_position = mommy.make(Position, song=self.song, week=self.last_week)
        self.some_week_position = mommy.make(Position, week=self.some_week)

        self.url = reverse('api:bet')
        self.client.force_authenticate(user=self.user)
        self.data = {'stake': 0, 'bet_type': 3, 'date': self.last_week.date,
                     'bets': [{'choice': 1, 'song': self.song.id}]}

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'No bet stake.'})

    def test_can_bet_only_on_last_week(self):
        mommy.make(Better, user=self.user, points=2)
        self.last_week_position = mommy.make(Position, song=self.song, week=self.last_week)
        self.some_week_position = mommy.make(Position, week=self.some_week)

        self.url = reverse('api:bet')
        self.client.force_authenticate(user=self.user)
        self.data = {'stake': 2, 'bet_type': 3, 'date': self.some_week.date,
                     'bets': [{'choice': 1, 'song': self.song.id}]}

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid week.'})

    def test_chooses_odd_based_on_choice(self):
        self.song_X = mommy.make(Song, name='foobar')
        self.better = mommy.make(Better, user=self.user, points=5)
        self.last_week_position = mommy.make(Position, song=self.song, week=self.last_week,
                                             odd_1='2.0')
        mommy.make(Position, song=self.song_X, week=self.last_week,
                   odd_x='8.0')

        self.url = reverse('api:bet')
        self.client.force_authenticate(user=self.user)
        self.data = {'stake': 3, 'bet_type': 3, 'date': self.last_week.date,
                     'bets': [{'choice': '1', 'song': self.song.id},
                              {'choice': 'X', 'song': self.song_X.id}]}

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.better.bet_set.all()[0].stake, 3)
        self.assertEqual(self.better.bet_set.all()[0].betitem_set.count(), 2)
        # querysets are generators, oh my...
        self.assertEqual(self.better.bet_set.all()[0].betitem_set.all().order_by('odd')[0].odd, 2.0)
        self.assertEqual(self.better.bet_set.all()[0].betitem_set.all().order_by('odd')[1].odd, 8.0)

    def test_bad_request(self):
        '''
        4 is invalid bet_type
        '''
        self.song_X = mommy.make(Song, name='foobar')
        self.better = mommy.make(Better, user=self.user, points=5)
        self.last_week_position = mommy.make(Position, song=self.song, week=self.last_week,
                                             odd_1='2.0')
        mommy.make(Position, song=self.song_X, week=self.last_week,
                   odd_x='8.0')
        self.some_week_position = mommy.make(Position, week=self.some_week)

        self.url = reverse('api:bet')
        self.client.force_authenticate(user=self.user)
        self.data = {'stake': 3, 'bet_type': 4, 'date': self.last_week.date,
                     'bets': [{'choice': '1', 'song': self.song.id},
                              {'choice': 'X', 'song': self.song_X.id}]}

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetOrCreateUserTest(TestCase):

    def setUp(self):
        self.view = SocialAuthView()

    def test_create_new_google_user(self):
        profile = {'email': 'foo@mail.com', 'given_name': 'Foo',
                   'family_name': 'Bar', 'picture': "http://www.foo.com"}
        self.view.get_or_create_user(profile)
        self.assertEqual(User.objects.all()[0].email, 'foo@mail.com')
        self.assertIsNotNone(User.objects.all()[0].better)

    def test_create_new_facebook_user(self):
        profile = {'id': '123', 'name': 'Foo Bar',
                   'picture': "http://www.foo.com"}
        self.view.get_or_create_user(profile)
        self.assertEqual(User.objects.all()[0].email, '123@facebook.com')
        self.assertIsNotNone(User.objects.all()[0].better)


class AbsoluteLeaderboardViewTest(APITestCase):

    def setUp(self):
        today = datetime.date.today()
        sunday = today + datetime.timedelta(days=-today.weekday() - 2, weeks=2)
        self.song = mommy.make(Song, name='foo')
        self.last_week = mommy.make(Week, date=sunday)
        self.some_week = mommy.make(Week, date=sunday-datetime.timedelta(weeks=2))

    def test_users_are_in_correct_order(self):
        self.user_top = mommy.make(User)
        self.better_top = mommy.make(Better, user=self.user_top, points=400)
        self.user = mommy.make(User)
        self.better = mommy.make(Better, user=self.user, points=40)
        self.url = reverse('api:leaderboard-absolute')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['users'][0]['user_id'], self.user_top.id)
        self.assertEqual(response.data['users'][0]['points'], 400)
        self.assertEqual(response.data['users'][1]['user_id'], self.user.id)


class RegisterTest(APITestCase):

    def setUp(self):
        self.url = reverse('api:register')
        User.objects.create_user(username='test2@test.com',
                                 email='test2@test.com')

    def test_create_account(self):
        """
        Valid data
        """
        data = {
            'email': 'test@test.com',
            'password': 'testpass',
            'username': 'Test',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(email='test@test.com').username, 'Test')

    def test_create_account_with_same_mail(self):
        data = {
            'email': 'test2@test.com',
            'password': 'testpass',
            'username': 'foo',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'User with same email already exists.'})

    def test_create_account_with_same_username(self):
        data = {
            'email': 'test2@testy.com',
            'password': 'testpass',
            'username': 'test2@test.com',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'username': ['This field must be unique.']})

    def test_create_account_without_required_field(self):
        data = {
            'email': 'test@test.com',
            'password': 'testpass',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ContactView(APITestCase):

    def setUp(self):
        self.url = reverse('api:contact')

    def test_contact(self):
        data = {
            'email': 'test@test.com',
            'name': 'testpass',
            'message': 'Test',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_incorrect_email(self):
        data = {
            'email': 'test@test',
            'name': 'testpass',
            'message': 'Test',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
