from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import os, time, simplejson
from datetime import datetime, timedelta, time

from social_auth import __version__ as version
from social_auth.utils import setting

def home_grid(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        ctx = {
            'version': version,
            'last_login': request.session.get('social_auth_last_login_backend'),
            'view': 'grid'
        }
        return render_to_response('index.html', ctx, RequestContext(request))
    else:
        ctx = {
            'version': version,
            'view': 'grid'
        }
        return render_to_response('index.html', ctx, RequestContext(request))

def home_map(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        ctx = {
            'version': version,
            'last_login': request.session.get('social_auth_last_login_backend'),
            'view': 'map'
        }
        return render_to_response('index.html', ctx, RequestContext(request))
    else:
        ctx = {
            'version': version,
            'view': 'map'
        }
        return render_to_response('index.html', ctx, RequestContext(request))

def home_two(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        ctx = {
            'version': version,
            'last_login': request.session.get('social_auth_last_login_backend')
        }
        return render_to_response('tdcv2.html', ctx, RequestContext(request))
    else:

        return render_to_response('tdcv2.html', {'version': version},
                                  RequestContext(request))


def feedback_form(request):
    """post feedback form and send email"""
    results = {'success':False}
    if(request.method == u'POST'):
        POST = request.POST
        send_mail('[CalHaps] Someone just left you a feedback!', POST['feedback']+" REPLY TO EMAIL: "+POST['replyToEmail'], 'caleventsinfo@gmail.com', EVENT_MASTERS, fail_silently=False)
        results['success'] = True
    json_results = simplejson.dumps(results)
    return HttpResponse(json_results, mimetype='application/json')

def add_event(request):
    """post new event and send email"""
    results = {'success':False}
    if(request.method == u'POST'):
        POST = request.POST
        emailBody = "Event Description: "+POST['eventDescription']+"--Event Title: "+POST['eventTitle']+"--When: "+POST['eventWhen']+"--Where: "+POST['eventWhere']+"--Host: "+POST['eventHost']
        send_mail('[CalHaps] Someone wants to add an event!', emailBody, 'caleventsinfo@gmail.com', EVENT_MASTERS, fail_silently=False)
        results['success'] = True
    json_results = simplejson.dumps(results)
    return HttpResponse(json_results, mimetype='application/json')
