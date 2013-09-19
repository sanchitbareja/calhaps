from django.db import models
from clubs.models import Club
import datetime

# email imports
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.template import Context
from django.utils.html import strip_tags
from calhaps.settings import EMAIL_HOST_USER, EVENT_MASTERS

# for implementing signals
from django.db.models.signals import post_save
from django.core import urlresolvers

TYPE_OF_EVENT_CHOICES = (
	('Parties', 'Parties'),
	('Concerts', 'Concerts'),
	('Greeklife', 'Greeklife'),
	('Sports', 'Sports'),
	('Philanthropy', 'Philanthropy'),
	('Performances', 'Performances'),
	('Conferences', 'Conferences'),
	('Movies', 'Movies'),
	('Food', 'Food'),
	('Green','Green'),
	('Celebrity','Celebrity'),
	('Exhibitions','Exhibitions'),
	('Others','Others')
	)

TYPE_OF_EVENT_CHOICES_HIDDEN = (
	('Parties', 'Parties'),
	('Concerts', 'Concerts'),
	('Greeklife', 'Greeklife'),
	('Sports', 'Sports'),
	('Philanthropy', 'Philanthropy'),
	('Performances', 'Performances'),
	('Conferences', 'Conferences'),
	('Movies', 'Movies'),
	('Food', 'Food'),
	('Green','Green'),
	('Celebrity','Celebrity'),
	('Exhibitions','Exhibitions'),
	('Others','Others'),
	('halloween','halloween'),
	)

class EventType(models.Model):
	type = models.CharField(max_length = 256, choices = TYPE_OF_EVENT_CHOICES_HIDDEN)

	def __unicode__(self):
		return self.type

class Location(models.Model):
	name = models.CharField(max_length=300)
	lat = models.DecimalField(max_digits=13, decimal_places=10)
	lng = models.DecimalField(max_digits=13, decimal_places=10)

	def __unicode__(self):
		return self.name

# Create your models here.
class Event(models.Model):
	title = models.TextField()
	description = models.TextField(null = True, blank = True)
	startTime = models.DateTimeField(editable=True, null=True, blank=True, default=datetime.datetime.now())
	club = models.ForeignKey(Club, blank = True, null = True)
	location = models.ForeignKey(Location, blank = True, null = True)
	image = models.URLField(blank = True, null = True)
	typeOfEvent = models.ManyToManyField(EventType, null = True, blank = True)
	advertise = models.DateTimeField(null = True, blank = True)
	readyForDisplay = models.BooleanField(default = False)
	addedBy = models.EmailField(null=True, blank=True)

	def __unicode__(self):
		return self.title

class FacebookEvent(models.Model):
	fbId = models.CharField(max_length=200, unique=True)
	title = models.TextField()
	description = models.TextField(null = True, blank = True)
	startTime = models.CharField(max_length=100)
	image = models.URLField(blank = True, null = True)

	def __unicode__(self):
		return self.title

class PersonalEvent(models.Model):
	fbEvent = models.ForeignKey(FacebookEvent)
	user = models.ForeignKey('users.User')
	rsvpStatus = models.CharField(max_length=100)

	def __unicode__(self):
		return self.fbEvent.title+" - "+self.user.username+" : "+self.rsvpStatus

# post save signal - will send email to relevant admins to add the event
def send_email_about_event(sender, **kwargs):
	obj = kwargs['instance']
	# send email to admins if event is not readyForDisplay to remind them about setting this
	if not obj.readyForDisplay:
		try:
			subject = '[CalHaps] A new event: '+str(obj.title)
			from_email = EMAIL_HOST_USER
			admins_to_email = EVENT_MASTERS
			admin_url = urlresolvers.reverse('admin:events_event_change', args=(obj.id,))
			
			my_context = Context({'admin_url':admin_url, 'event_title':obj.title, 'event_description':obj.description})
			html_content = render_to_string('emails/email_notification_template_new_event.html', my_context)
			text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
			
			# create the email, and attach the HTML version as well
			msg = EmailMultiAlternatives(subject, text_content, from_email, admins_to_email)
			msg.attach_alternative(html_content, "text/html")
			msg.send()
		except Exception as e:
			print e
			raise e
	else:
		if obj.addedBy:
			try:
				subject = '[CalHaps] Your event ('+obj.title+') has been successfully added!'
				from_email = EMAIL_HOST_USER
				to_email = [obj.addedBy]

				my_context = Context({'event_title':obj.title,'event_description':obj.description,'event_start_time':obj.startTime,'event_club':obj.club.name})
				html_content = render_to_string('emails/email_notification_template_approved_event.html', my_context)
				text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.

				# create the email, and attach the HTML version as well
				msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
				msg.attach_alternative(html_content, "text/html")
				msg.send()
			except Exception as e:
				print e
				raise e

post_save.connect(send_email_about_event , sender=Event)
