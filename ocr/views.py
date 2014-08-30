from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404
from django.template import RequestContext


# Create your views here.
def home(request):
    """
    Gets data from file processor log based on the current selection
    """
    print 'reched home'
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))


# Create your views here.
def signup(request):
    """
    Gets data from file processor log based on the current selection
    """
    print 'reched signup'
    return render_to_response('signup.html', locals(), context_instance=RequestContext(request))

# Create your views here.
def signin(request):
    """
    Gets data from file processor log based on the current selection
    """
    print 'reched signin'
    return render_to_response('signin.html', locals(), context_instance=RequestContext(request))
