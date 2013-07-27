from django.contrib import admin
from events.models import Event, Location, EventType, FacebookEvent, PersonalEvent

#register the admin site
class EventTypeAdmin(admin.ModelAdmin):
	list_display = ['type']

class LocationAdmin(admin.ModelAdmin):
	list_display = ['name', 'lat', 'lng']

class EventAdmin(admin.ModelAdmin):
	list_display = ['title','description','startTime', 'club','image', 'location','advertise']

class FacebookEventAdmin(admin.ModelAdmin):
	list_display = ['fbId','title','description','startTime','image']

class PersonalEventAdmin(admin.ModelAdmin):
	list_display = ['fbEvent','user','rsvpStatus']

admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(FacebookEvent, FacebookEventAdmin)
admin.site.register(PersonalEvent, PersonalEventAdmin)