from django.conf.urls import url, include
from api import(
    LastWeekViewSet, BetView, AddBetView, BetHistoryViewSet, SongViewSet,
    PositionViewSet, WeekViewSet, RegisterView,
    GoogleAuthView,
    FacebookAuthView,
    SocialUserView,
    AbsoluteLeaderboardView,
    MyBetsViewSet,
    CommentViewSet,
    WeekTopSet,
    ContactView
)
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register('lastweek', LastWeekViewSet, base_name='lastweek')
router.register('history', BetHistoryViewSet, base_name='history')
router.register('song', SongViewSet, base_name='song')
router.register('mybets', MyBetsViewSet, base_name='mybets')
router.register('bestoftheweek', WeekTopSet, base_name='bestoftheweek')

router.register('weeks', WeekViewSet, base_name='weeks')

weeks_router = routers.NestedSimpleRouter(router, r'weeks', lookup='weeks')
weeks_router.register(r'positions', SongViewSet, base_name='positions')

positions_router = routers.NestedSimpleRouter(weeks_router, r'positions', lookup='positions')
positions_router.register(r'comments', CommentViewSet, base_name='comments')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(weeks_router.urls)),
    url(r'^', include(positions_router.urls)),
    url(r'bet/$', BetView.as_view(), name='bet'),
    url(r'addbet/$', AddBetView.as_view(), name='bet'),
    url(r'position/(?P<pk>[0-9]+)/$', PositionViewSet.as_view(),
        name='position'),
    url(r'register/$', RegisterView.as_view(), name='register'),
    url(r'login/google-oauth2/$', GoogleAuthView.as_view()),
    url(r'login/facebook/$', FacebookAuthView.as_view()),
    url(r'socialuser/$', SocialUserView.as_view()),
    url(r'leaderboard/$', AbsoluteLeaderboardView.as_view(), name='leaderboard-absolute'),
    url(r'contact/$', ContactView.as_view(), name='contact'),
]
urlpatterns += router.urls
