from django.contrib import admin
from events.models import Event, Location, EventType

#register the admin site
class EventTypeAdmin(admin.ModelAdmin):
	list_display = ['type']

class LocationAdmin(admin.ModelAdmin):
	list_display = ['name', 'lat', 'lng']

class EventAdmin(admin.ModelAdmin):
	list_display = ['title','description','startTime', 'club','image', 'location','advertise']

admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)