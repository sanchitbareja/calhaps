# tastypie imports
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpForbidden

# imports for haystack
from django.conf.urls.defaults import *
from django.core.paginator import Paginator, InvalidPage
from tastypie.utils import trailing_slash
from django.http import Http404

# misc
from django.db.models import Q
from clubs.models import Club
from events.models import Event, Location
import datetime

class ClubResource(ModelResource):
    class Meta:
        queryset = Club.objects.all()
        resource_name = 'clubs'
        # Add it here.
        # authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

        allowed_methods = ['get']
        filtering = {
            "username": ("exact")
        }

    def dehydrate(self, bundle):
        """
        Return a list of clubs formatted according to what the developer expects
        """
        # no renaming required for 'name'
        bundle.data['name'] = bundle.obj.name

        # no renaming required for 'description'
        bundle.data['description'] = bundle.obj.description

        # no renaming required for 'typeOfOrganization'
        bundle.data['typeOfOrganization'] = bundle.obj.typeOfOrganization

        # no renaming required for 'urlPersonal'
        bundle.data['urlPersonal'] = bundle.obj.urlPersonal

        # rename 'image' to 'imageUrl'
        bundle.data['imageUrl'] = bundle.obj.image
        del(bundle.data['image'])

        # no renaming required for 'founded'
        bundle.data['founded'] = bundle.obj.founded

        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "response"
        data['response'] = {"clubs":data['objects']}
        del(data['objects'])
        return data

    def determine_format(self, request):
        return 'application/json'

class EventResource(ModelResource):
    """
    Return a list of events
    """

    class Meta:
        # filter events from current date
        queryset = Event.objects.all().filter(readyForDisplay=True)
        resource_name = 'events'
        # Add it here.
        # authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

        allowed_methods = ['get', 'post']
        limit = 0
        excludes = ['readyForDisplay']
        filtering = {
            "username": ("exact")
        }

    def dehydrate(self, bundle):
        # no renaming required for 'title'
        bundle.data['title'] = bundle.obj.title

        # no renaming required for 'description'
        bundle.data['description'] = bundle.obj.description

        # no renaming required for 'startTime'
        bundle.data['startTime'] = bundle.obj.startTime

        # only return the club's 'id'
        bundle.data['club'] = bundle.obj.club.id

        # only return the lat and lng of the event location without requiring a location resource
        bundle.data['location'] = {'lat':bundle.obj.location.lat,'lng':bundle.obj.location.lng}

        # rename 'image' to 'imageUrl'
        bundle.data['imageUrl'] = bundle.obj.image
        del(bundle.data['image'])

        # return a list for 'typeOfEvent' - based on the manyToMany model
        bundle.data['typeOfEvent'] = [{"type":eventType.type} for eventType in bundle.obj.typeOfEvent.all()]

        # no renaming required for 'advertise'
        bundle.data['advertise'] = bundle.obj.advertise

        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # rename "objects" to "response"
        data['response'] = {"events":data['objects']}
        del(data['objects'])
        return data

    def obj_create(self, bundle, **kwargs):
        """
        Post creates a new event but doesn't show it to public yet.
        - sends email out to relevant people to add event manually.
        """
        try:
            event_title = bundle.data['title']
            event_description = bundle.data['description']
            if 'addedBy' in bundle.data.keys():
                event_added_by = bundle.data['addedBy']
                new_event = Event(title=event_title,description=event_description, addedBy=event_added_by)
            else:
                new_event = Event(title=event_title,description=event_description)
            print "11"
            print new_event
            new_event.save()
            print "22"
            bundle.obj = new_event
        except Exception as e:
            print e
            raise ImmediateHttpResponse(HttpForbidden("Invalid POST bundle."))
        return bundle

    def determine_format(self, request):
        return 'application/json'
