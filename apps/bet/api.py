import requests
import json

from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import mail_admins


from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler

from .models import Week, Position, BetItem, Song, Bet, Better, Comment
from .serializers import(
    WeekSerializer,
    AddBetSerializer, BetHistorySerializer, SongSerializer, PositionSerializer,
    WeeksSerializer, BetSerializer, UserSerializer,
    MyBetSerializer, MyBetsSerializer, CommentSerializer,
    WeekTopSerializer, ContactSerializer
)


class BetView(GenericAPIView):

    serializer_class = BetSerializer

    def post(self, request):
        serialized = BetSerializer(data=request.DATA)
        if serialized.is_valid():
            better = request.user.better
            if serialized.data['stake'] <= 0:
                return Response(
                    {'error': 'No bet stake.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                week = Week.objects.get(date=serialized.data['date'])
            except Week.DoesNotExist:
                return Response({'error': 'No such week.'}, status=status.HTTP_400_BAD_REQUEST)
            # Currently only last week is allowed, this will change in the future.
            if week != Week.latest():
                return Response({'error': 'Invalid week.'}, status=status.HTTP_400_BAD_REQUEST)

            if better.points - serialized.data['stake'] < 0:
                return Response({'error': 'Insufficient points.'},
                                status=status.HTTP_400_BAD_REQUEST)

            better.points -= serialized.data['stake']

            bet = Bet.objects.create(better=better, bet_type=serialized.data['bet_type'],
                                     stake=serialized.data['stake'], week=week)
            for serialized_bet in serialized.data['bets']:
                song = Song.objects.get(id=serialized_bet['song'])
                position = Position.objects.get(week=week, song=song)
                odd = 'odd_' + serialized_bet['choice'].lower()
                BetItem.objects.create(
                    bet=bet, song=song, odd=getattr(position, odd),
                    choice=serialized_bet['choice'])
            better.save()
            return Response(
                status=status.HTTP_201_CREATED
            )

        return Response(
            serialized._errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AddBetView(GenericAPIView):

    serializer_class = AddBetSerializer

    def post(self, request):
        serialized = AddBetSerializer(data=request.DATA)
        if serialized.is_valid():
            data = serialized.data
            bet_id = data['bet_id']
            bet = Bet.objects.get(id=bet_id)
            song_id = data['song']
            song = Song.objects.get(id=song_id)
            choice = data['choice']
            BetItem.objects.create(bet=bet, song=song, choice=choice)
            return Response(
                status=status.HTTP_201_CREATED
            )
        return Response(
            serialized.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LastWeekViewSet(ReadOnlyModelViewSet):
    serializer_class = WeekSerializer
    """
    TODO: check when billboard chart comes out
    today = datetime.date.today()
    sunday = today + datetime.timedelta(days=-today.weekday() - 2, weeks=1)
    # billboard gives its chart one week in advance
    sunday = sunday + datetime.timedelta(days=7)
    """
    queryset = Week.objects.all().order_by('-date')[:1]


class BetHistoryViewSet(ReadOnlyModelViewSet):
    serializer_class = BetHistorySerializer

    def get_queryset(self):
        user = self.request.user.better
        return Bet.objects.filter(user=user)


class SongViewSet(ReadOnlyModelViewSet):
    serializer_class = SongSerializer
    queryset = Song.objects.all()


class PositionViewSet(GenericAPIView):
    serializer_class = PositionSerializer

    def get(self, request, pk):
        song = Song.objects.get(id=pk)
        positions = PositionSerializer(song.position_set.all(), many=True)
        return Response(
            positions.data,
            status=status.HTTP_200_OK
        )


class WeekViewSet(ReadOnlyModelViewSet):
    queryset = Week.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return WeeksSerializer
        if self.action == 'retrieve':
            return WeekSerializer
        return WeekSerializer


class RegisterView(GenericAPIView):
    throttle_classes = ()
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        serialized = UserSerializer(data=request.DATA)
        if serialized.is_valid():
            try:
                User.objects.get(email=serialized.data['email'])
                return Response({'error': 'User with same email already exists.'},
                                status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                pass
            user = User.objects.create_user(
                serialized.data['username'],
                serialized.data['email'],
                serialized.data['password'],
                first_name=serialized.data['username']
            )
            Better.objects.create(user=user)
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({'token': token.decode('unicode_escape')},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class SocialAuthView(APIView):

    throttle_classes = ()
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get_or_create_user(self, profile):
        user = None
        if 'email' in profile or 'name' in profile:
            try:
                # google
                email = profile['email']
                first_name = profile['given_name']
                last_name = profile['family_name']
            except KeyError:
                # facebook
                email = profile['email']
                first_name = profile['name'].split()[0]
                last_name = profile['name'].split()[1]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create(username=email,
                                           first_name=first_name,
                                           last_name=last_name,
                                           email=email)
            if not hasattr(user, 'better'):
                Better.objects.create(user=user, points=100)
        return user


class GoogleAuthView(SocialAuthView):

    def post(self, request):
        access_token_url = 'https://accounts.google.com/o/oauth2/token'
        people_api_url = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'

        payload = dict(client_id=request.data['clientId'],
                       redirect_uri=request.data['redirectUri'],
                       client_secret=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                       code=request.data['code'],
                       grant_type='authorization_code')

        # Step 1. Exchange authorization code for access token.
        r = requests.post(access_token_url, data=payload)
        token = json.loads(r.text)
        headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}

        # Step 2. Retrieve information about the current user.
        r = requests.get(people_api_url, headers=headers)
        profile = json.loads(r.text)

        user = self.get_or_create_user(profile)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'token': token.decode('unicode_escape')},
                        status=status.HTTP_200_OK)


class FacebookAuthView(SocialAuthView):

    def post(self, request):
        access_token_url = 'https://graph.facebook.com/v2.4/oauth/access_token'
        people_api_url = 'https://graph.facebook.com/v2.4/me?fields=id,email,name'

        payload = dict(client_id=request.data['clientId'],
                       redirect_uri=request.data['redirectUri'],
                       client_secret=settings.SOCIAL_AUTH_FACEBOOK_SECRET,
                       code=request.data['code'],
                       scope='email',
                       )

        # Step 1. Exchange authorization code for access token.
        r = requests.post(access_token_url, data=payload)
        token = json.loads(r.text)
        headers = {'Authorization': 'Bearer {0}'.format(token['access_token']), 'scope': 'email'}

        # Step 2. Retrieve information about the current user.
        r = requests.get(people_api_url, headers=headers)
        profile = json.loads(r.text)

        user = self.get_or_create_user(profile)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'token': token.decode('unicode_escape')}, status=status.HTTP_200_OK)


class SocialUserView(GenericAPIView):

    def get(self, request):
        name = request.user.first_name + " " + request.user.last_name
        betting_funds = request.user.better.points

        return Response({'name': name, 'betting_funds': betting_funds},
                        status=status.HTTP_200_OK)


class AbsoluteLeaderboardView(GenericAPIView):

    def get(self, request):
        betters = Better.objects.all().order_by('-points')[:100]
        serialized_betters = []
        for better in betters:
            serialized_better = {}
            serialized_better['name'] = better.user.first_name + " " + better.user.last_name
            serialized_better['points'] = better.points
            serialized_better['user_id'] = better.user.id
            serialized_betters.append(serialized_better)
        return Response({'users': serialized_betters}, status=status.HTTP_200_OK)


class MyBetsViewSet(ReadOnlyModelViewSet):

    def get_serializer_class(self):
        if self.action == 'list':
            return MyBetsSerializer
        else:
            return MyBetSerializer

    def get_queryset(self):
        return Bet.objects.filter(better=self.request.user.better)


class CommentViewSet(ModelViewSet):
    model = Comment
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()

    def create(self, request, pk=None, weeks_pk=None, positions_pk=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            position = Position.objects.get(week=weeks_pk, position=positions_pk)
            comment = Comment.objects.create(text=serializer.validated_data['comment'],
                                             creator=request.user,
                                             position=position)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class WeekTopSet(ReadOnlyModelViewSet):
    serializer_class = WeekTopSerializer

    def get_queryset(self):
        return (Song.objects.filter(position__position=1))


class ContactView(CreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = ()

    def create(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']
            body = '{} - {} \n{}'.format(name, email, message)
            mail_admins("Contact us - songbet", body)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
