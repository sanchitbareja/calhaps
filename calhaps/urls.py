from django.conf.urls import patterns, include, url
from events.views import home_grid, home_map, home_two
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# API
from tastypie.api import Api
from api.api import ClubResource
from api.api import EventResource
from api.views import logout_view, login_error

v1_api = Api(api_name='v1')
v1_api.register(ClubResource())
v1_api.register(EventResource())

urlpatterns = patterns('',
    # Examples:
    url(r'^$', home_grid, name='home-grid'),
    url(r'^map/$', home_map, name='home-map'),
    url(r'^tdcv2/$', home_two, name='tdcv2'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^login-error/$', login_error, name='login-error'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # social-auth-urls
    url(r'', include('social_auth.urls')),
    url(r'^done/$', home_grid, name='home_grid'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # v1 API
    url(r'^api/', include(v1_api.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

