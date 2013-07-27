# Create your views here.
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/')

def login_error(request):
	print request
	return redirect('/')