from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
import os, time, simplejson
from datetime import datetime, timedelta, time

def home(request):
    return render_to_response('index.html', ctx, context_instance=RequestContext(request))