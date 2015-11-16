from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
import spirit.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bbet.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('apps.bet.urls', namespace='api')),
    url(r'^app/', views.index, name='index'),
    url(r'^home/', views.home, name='home'),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^community/', include(spirit.urls)),
)
