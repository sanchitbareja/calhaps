# tastypie imports
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpForbidden, HttpCreated

# imports for haystack
from django.conf.urls.defaults import *
from django.core.paginator import Paginator, InvalidPage
from tastypie.utils import trailing_slash
from django.http import Http404, HttpResponse

# misc
from django.db.models import Q
from clubs.models import Club
from events.models import Event, Location
from favorites.models import Favorite
from users.models import User
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

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(EventResource, self).build_filters(filters)

        if "date" in filters:
            try:
                filter_date = filters['date']
                date_array = filter_date.split('-')
                filter_start_date = datetime.date(int(date_array[0]),int(date_array[1]),int(date_array[2]))
                filter_end_date = filter_start_date + datetime.timedelta(days=1)

                # make sure the date is correct
                sqs = Event.objects.filter(startTime__gte=filter_start_date).filter(startTime__lte=filter_start_date+datetime.timedelta(days=1))
            except:
                sqs = []
            if "pk__in" not in orm_filters.keys():
                orm_filters["pk__in"] = []
            orm_filters["pk__in"] = orm_filters["pk__in"] + [i.pk for i in sqs]

        if "event_filters" in filters:
            try:
                event_filters = filters['event_filters']
                # remove white spaces and capitalize first letter
                event_filters_array = [event_filter.strip().title() for event_filter in event_filters.split(',')]

                sqs = Event.objects.filter(typeOfEvent__type__in=event_filters_array)
            except:
                sqs = []
            if "pk__in" not in orm_filters.keys():
                orm_filters["pk__in"] = []
            orm_filters["pk__in"] = orm_filters["pk__in"] + [i.pk for i in sqs]

        if "date" in filters and "event_filters" in filters:
            try:
                filter_date = filters['date']
                date_array = filter_date.split('-')
                filter_start_date = datetime.date(int(date_array[0]),int(date_array[1]),int(date_array[2]))
                filter_end_date = filter_start_date + datetime.timedelta(days=1)

                event_filters = filters['event_filters']
                # remove white spaces and capitalize first letter
                event_filters_array = [event_filter.strip().title() for event_filter in event_filters.split(',')]

                sqs = Event.objects.filter(startTime__gte=filter_start_date).filter(startTime__lte=filter_start_date+datetime.timedelta(days=1)).filter(typeOfEvent__type__in=event_filters_array)
            except:
                sqs = []
            if "pk__in" not in orm_filters.keys():
                orm_filters["pk__in"] = []
            orm_filters["pk__in"] = [i.pk for i in sqs]

        return orm_filters

    def dehydrate(self, bundle):
        # no renaming required for 'title'
        bundle.data['title'] = bundle.obj.title

        # no renaming required for 'description'
        bundle.data['description'] = bundle.obj.description

        # no renaming required for 'startTime'
        bundle.data['startTime'] = bundle.obj.startTime

        # club related date
        bundle.data['club'] = {}
        bundle.data['club']['id'] = bundle.obj.club.id
        bundle.data['club']['name'] = bundle.obj.club.name
        bundle.data['club']['description'] = bundle.obj.club.description
        bundle.data['club']['typeOfOrganization'] = bundle.obj.club.typeOfOrganization
        bundle.data['club']['urlPersonal'] = bundle.obj.club.urlPersonal
        bundle.data['club']['imageUrl'] = bundle.obj.club.image
        bundle.data['club']['founded'] = bundle.obj.club.founded

        # only return the lat and lng of the event location without requiring a location resource
        bundle.data['location'] = {'lat':bundle.obj.location.lat,'lng':bundle.obj.location.lng, 'name':bundle.obj.location.name}

        # rename 'image' to 'imageUrl'
        bundle.data['imageUrl'] = bundle.obj.image
        del(bundle.data['image'])

        # return a list for 'typeOfEvent' - based on the manyToMany model
        bundle.data['typeOfEvent'] = [{"type":eventType.type} for eventType in bundle.obj.typeOfEvent.all()]

        # no renaming required for 'advertise'
        bundle.data['advertise'] = bundle.obj.advertise

        # sends a list of favorites for the event
        bundle.data['favorites'] = [favorite.user.id for favorite in Favorite.objects.filter(event__id=bundle.obj.id)]

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

class FavoriteResource(ModelResource):
    class Meta:
        queryset = Favorite.objects.all()
        resource_name = 'favorites'
        # Add it here.
        # authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        allowed_methods = ['post']

    def dehydrate(self, bundle):
        event = Event.objects.get(id=bundle.obj.event.id)
        # no renaming required for 'title'
        bundle.data['title'] = bundle.obj.event.title

        # no renaming required for 'description'
        bundle.data['description'] = bundle.obj.event.description

        # no renaming required for 'startTime'
        bundle.data['startTime'] = bundle.obj.event.startTime

        # club related date
        bundle.data['club'] = {}
        bundle.data['club']['id'] = bundle.obj.event.club.id
        bundle.data['club']['name'] = bundle.obj.event.club.name
        bundle.data['club']['description'] = bundle.obj.event.club.description
        bundle.data['club']['typeOfOrganization'] = bundle.obj.event.club.typeOfOrganization
        bundle.data['club']['urlPersonal'] = bundle.obj.event.club.urlPersonal
        bundle.data['club']['imageUrl'] = bundle.obj.event.club.image
        bundle.data['club']['founded'] = bundle.obj.event.club.founded

        # only return the lat and lng of the event location without requiring a location resource
        bundle.data['location'] = {'lat':bundle.obj.event.location.lat,'lng':bundle.obj.event.location.lng, 'name':bundle.obj.event.location.name}

        # rename 'image' to 'imageUrl'
        bundle.data['imageUrl'] = bundle.obj.event.image

        # return a list for 'typeOfEvent' - based on the manyToMany model
        bundle.data['typeOfEvent'] = [{"type":eventType.type} for eventType in bundle.obj.event.typeOfEvent.all()]

        # no renaming required for 'advertise'
        bundle.data['advertise'] = bundle.obj.event.advertise

        # sends a list of favorites for the event
        bundle.data['favorites'] = [favorite.user.id for favorite in Favorite.objects.filter(event__id=bundle.obj.event.id)]

        return bundle

    def obj_create(self, bundle, **kwargs):
        """
        Post favorites an event for the user
        if 'delete' is in param, then we delete that post instead
        """
        try: 
            if bundle.data.get('delete',False):
                try:
                    print bundle.data
                    event_id = bundle.data['event']
                    user_id = bundle.data['user']
                    event = Event.objects.get(id=event_id)
                    user = User.objects.get(id=user_id)
                    old_favorite = Favorite.objects.get(event=event, user=user)
                    old_favorite.delete()
                    # return some random Favorite object
                    bundle.obj = Favorite.objects.all()[0]
                except Exception as e:
                    print e
                    raise ImmediateHttpResponse(HttpForbidden("Unable to unfavorite event. Please try again."))
                return bundle
            else:
                try:
                    print bundle.data
                    event_id = bundle.data['event']
                    user_id = bundle.data['user']
                    event = Event.objects.get(id=event_id)
                    user = User.objects.get(id=user_id)
                    if len(Favorite.objects.filter(event=event, user=user)) == 0:
                        new_favorite = Favorite(event=event, user=user)
                        new_favorite.save()
                    else:
                        new_favorite = Favorite.objects.filter(event=event, user=user)[0]
                    bundle.obj = new_favorite
                except Exception as e:
                    print e
                    raise ImmediateHttpResponse(HttpForbidden("Invalid POST bundle."))
                return bundle
        except Exception as e:
            print e
            raise ImmediateHttpResponse(HttpForbidden("Unable to perform request. Please try again."))

    def determine_format(self, request):
        return 'application/json'

