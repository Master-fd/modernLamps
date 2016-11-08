#conding utf8
from django.shortcuts import render

# Create your views here.

from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response

def home(request):
    return render_to_response('home.html');
