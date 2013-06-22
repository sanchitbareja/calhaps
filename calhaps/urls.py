from django.conf.urls import patterns, include, url
from events.views import home

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# API
from tastypie.api import Api
from api.api import ClubResource
from api.api import LocationResource
from api.api import EventResource

v1_api = Api(api_name='v1')
v1_api.register(ClubResource())
v1_api.register(EventResource())
v1_api.register(LocationResource())

urlpatterns = patterns('',
    # Examples:
    url(r'^$', home),
    # url(r'^calhaps/', include('calhaps.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # v1 API
    url(r'^api/', include(v1_api.urls)),
)
