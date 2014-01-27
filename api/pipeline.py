from social_auth.backends.facebook import FacebookBackend
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files import File
from urllib2 import urlopen
from events.models import FacebookEvent, PersonalEvent
from users.models import User
import simplejson, urllib


def get_user_profile_pic(backend, details, response, social_user, uid, user, *args, **kwargs):
    url = None
    print response
    print backend
    print user
    if backend.__class__ == FacebookBackend:
        profile_pic_url = "https://graph.facebook.com/%s/picture?type=large" % response['id']
        thumbnail_profile_pic_url = "https://graph.facebook.com/%s/picture?type=small" % response['id']
        user.profile_pic = profile_pic_url
        user.thumbnail_profile_pic = thumbnail_profile_pic_url
        user.save()

    if profile_pic_url:
        print "profile_pic_url"
        print profile_pic_url

    if thumbnail_profile_pic_url:
        print "thumbnail_profile_pic"
        print thumbnail_profile_pic_url
    

def get_user_events(backend, details, response, social_user, uid, user, *args, **kwargs):
    url = None
    if backend.__class__ == FacebookBackend:
        query = "SELECT name, start_time, timezone, description, pic, location, eid FROM event WHERE eid IN (SELECT eid FROM event_member WHERE uid="+str(response['id'])+")"
        params = urllib.urlencode({'q': query, 'access_token': str(response['access_token'])})
        url = "https://graph.facebook.com/fql?"+params
        print url
        events_data = simplejson.loads(urlopen(url).read())
        print events_data
        for event in events_data['data']:
            old_event = FacebookEvent.objects.filter(fbId=event['eid'])
            if len(old_event) > 0:
                old_event = old_event[0]
            else:
                if 'description' in event.keys():
                    old_event = FacebookEvent(fbId=event['eid'],title=event['name'],description=event['description'],image=event['pic'],startTime=event['start_time'])
                else:
                    old_event = FacebookEvent(fbId=event['eid'],title=event['name'],image=event['pic'],startTime=event['start_time'])
                old_event.save()
            # new_event_association = PersonalEvent.objects.filter(user=user, fbEvent=old_event, rsvpStatus=event['rsvp_status'])
            # if len(new_event_association) == 0:
            #     new_event_association = PersonalEvent(user=user, fbEvent=old_event, rsvpStatus=event['rsvp_status'])
            #     new_event_association.save()
        print events_data

# def get_user_network(backend, details, response, social_user, uid, user, *args, **kwargs):
#     url = None
#     if backend.__class__ == FacebookBackend:
#         url = "https://graph.facebook.com/fql?q=select%20affiliations%20from%20user%20where%20uid="+str(response['id'])+"&access_token="+response['access_token']
#         print urlopen(url).read()

# def get_user_pages(backend, details, response, social_user, uid, user, *args, **kwargs):
#     url = None
#     if backend.__class__ == FacebookBackend:
#         url = "https://graph.facebook.com/fql?q=select%20page_id%20from%20page_admin%20where%20uid="+str(response['id'])+"&access_token="+response['access_token']
#         print urlopen(url).read()