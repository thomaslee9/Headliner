# 17-437 Team30
# Headliner App
# views.py

from django.shortcuts import render
from django.shortcuts import redirect, reverse

from headliner.forms import LoginForm
from headliner.forms import RegisterForm

from django.contrib.auth.decorators import login_required
from headliner.models import Event
from django.utils import timezone
from headliner.forms import EventForm
from django.http import HttpResponse


import json
import datetime
# Create your views here.

def login_action(request):
    context = {}
    if request.user.is_authenticated:
        context['status'] = "User is authenticated."
        return redirect(reverse('global'))
    
    return render(request, 'headliner/login.html', {})


def register_action(request):
    context = {}

    return render(request, 'headliner/register.html', {})



@login_required
def global_action(request):
    user = request.user
    if request.method == 'GET':
        event_form = EventForm()
        events = Event.objects.all().order_by('-creation_time')
        context = {'user': user, 'form': event_form, 'entries': events}
        return render(request, 'headliner/global.html', context)

    entry = Event()
    entry.created_by=request.user
    entry.creation_time=timezone.now()

    event_form = EventForm(request.POST)
    if not event_form.is_valid():
        context = { 'form': event_form, 'user':user }
        return render(request, 'headliner/global.html', context)
    entry.post_input_text = event_form.cleaned_data['post_input_text']
    entry.save()
    posts = Event.objects.all().order_by('-creation_time')

    context = { 'user': user, 'form': event_form, 'entries': posts}
    return render(request, 'headliner/global.html', context)

def get_global(request):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    response_data = {}
    response_data['events'] = []
    for event_item in Event.objects.all():
        event_item = {
            'id': event_item.id,
            'text': event_item.event_description,
            'username': event_item.created_by.username,
            'first_name': event_item.created_by.first_name,
            'last_name': event_item.created_by.last_name,
            'creation_time': event_item.creation_time.isoformat(),
        }
        response_data['events'].append(event_item)

    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')

def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{"error": "' + message + '"}'
    return HttpResponse(response_json, content_type='application/json', status=status)