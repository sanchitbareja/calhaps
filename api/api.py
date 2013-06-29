# tastypie imports
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie import fields

# imports for haystack
from django.conf.urls.defaults import *
from django.core.paginator import Paginator, InvalidPage
from tastypie.utils import trailing_slash
from django.http import Http404

# misc
from django.db.models import Q
from clubs.models import Club
from events.models import Event, Location

class ClubResource(ModelResource):
    class Meta:
        queryset = Club.objects.all()
        resource_name = 'club'
        # Add it here.
        # authentication = BasicAuthentication()
        authorization = Authorization()
        filtering = {
            "username": ("exact")
        }

    def determine_format(self, request):
        return 'application/json'

class LocationResource(ModelResource):
    class Meta:
        queryset = Location.objects.all()
        resource_name = 'location'
        # Add it here.
        authentication = BasicAuthentication()
        # authorization = Authorization()

    def determine_format(self, request):
        return 'application/json'

class EventResource(ModelResource):
    location = fields.ForeignKey(LocationResource, 'location', full=True)
    club = fields.ForeignKey(ClubResource, 'club', full=True)

    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
        # Add it here.
        # authentication = BasicAuthentication()
        authorization = Authorization()
        filtering = {
            "username": ("exact")
        }

    def determine_format(self, request):
        return 'application/json'
