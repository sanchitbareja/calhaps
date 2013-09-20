from django.db import models
from events.models import Event
from users.models import User

class Favorite(models.Model):
	event = models.ForeignKey(Event, blank = True, null = True)
	user = models.ForeignKey(User, blank = True, null = True)

	def __unicode__(self):
		return "(event, user): ("+str(self.event.id)+", "+str(self.user.id)+")"
