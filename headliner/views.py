# 17-437 Team30
# Headliner App
# views.py

from django.shortcuts import render
from django.shortcuts import redirect , get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404

from headliner.forms import LoginForm
from headliner.forms import RegisterForm, RSVPForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from headliner.models import Event, Profile
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
    # Login to Headliner
    if request.method == 'GET':
        context = {'status': ""}
        context['form'] = LoginForm()
        return render(request, 'headliner/login.html', context)
    # Check Login Fields Exist
    if "username" not in request.POST:
        context = {'status': "Username is Required"}
        context['form'] = LoginForm()
        return render(request, "headliner/login.html", context)

    if "password" not in request.POST:
        context = {'status': "Password is Required"}
        context['form'] = LoginForm()
        return render(request, "headliner/login.html", context)

    # Parse Login Form
    form = LoginForm(request.POST)
    status = "Log-in to Headliner"

    if not form.is_valid():
        context = {'status': "Invalid Username or Password"}
        context['form'] = LoginForm(request.POST)
        return render(request, "headliner/login.html", context)

    # Authenticate User
    newUser = authenticate(username=form.cleaned_data['username'],
                           password=form.cleaned_data['password'])
    status = "Successfully Logged In"

    # Login User
    login(request, newUser)
    context['form'] = form
    context['status'] = status
    profile, created = Profile.objects.get_or_create(user=newUser)
    profile.save()



    return redirect(reverse('global'))


def register_action(request):
    context = {}
    # Register to Headiner
    if request.method == 'GET':
        context = {'status': ""}
        context['form'] = RegisterForm()
        return render(request, "headliner/register.html", context)

    # Check Register Fields Exist
    if "username" not in request.POST:
        context = {'status': "Username is Required"}
        context['form'] = RegisterForm()
        return render(request, "headliner/register.html", context)

    if "password" not in request.POST:
        context = {'status': "Password is Required"}
        context['form'] = RegisterForm()
        return render(request, "headliner/register.html", context)

    if "confirm_password" not in request.POST:
        context = {'status': "Correct Confirmation of Password is Required"}
        context['form'] = RegisterForm()
        return render(request, "headliner/register.html", context)

    if "email" not in request.POST:
        context = {'status': "E-mail is Required"}
        context['form'] = RegisterForm()
        return render(request, "headliner/register.html", context)

    if "first_name" not in request.POST:
        context = {'status': "First Name is Required"}
        context['form'] = RegisterForm()
        return render(request, "headliner/register.html", context)

    if "last_name" not in request.POST:
        context = {'status': "Last Name is Required"}
        context['form'] = RegisterForm()
        return render(request, "headliner/register.html", context)

    # Parse Register Form
    form = RegisterForm(request.POST)
    status = "Headliner Registration"

    if not form.is_valid():
        context = {'status': "Invalid Username or Password"}
        context['form'] = RegisterForm()
        context['error'] = "Error: Registration Form is not Valid"
        return render(request, "headliner/register.html", context)

    # Create New User Object
    newUser = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    newUser.save()

    # Authenticate New User
    newUser = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    # Login New User
    login(request, newUser)

    context['form'] = form
    context['status'] = status
    profile, created = Profile.objects.get_or_create(user=newUser)
    profile.save()

    return redirect(reverse('global'))

@login_required
def logout_action(request):
    logout(request)

    context = {'status': "Successfully Logged Out"}
    context['form'] = LoginForm()

    return redirect(reverse('login'))

@login_required
def get_photo(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if not event.event_picture:
        raise Http404

    return HttpResponse(event.event_picture)


@login_required
def event_action(request, event_id):
    context = {}
    event = get_object_or_404(Event, id=event_id)
    context['event'] = event
    context['rsvp_name'] = 'RSVP'
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
        return render(request, 'headliner/event.html', context)
    is_attending = profile.attending.filter(id=event.id).exists()

    if request.method == 'GET':
        rsvp_form = RSVPForm()
        context['form'] = rsvp_form
        if not is_attending:
            pass
        else:
            context['rsvp_name'] = 'Un-RSVP'
        return render(request, 'headliner/event.html', context)

    rsvp_form = RSVPForm(request.POST)
    if not rsvp_form.is_valid():
        context = { 'form': rsvp_form, 'event':event }
        return render(request, 'headliner/event.html', context)

    if not is_attending:
        profile.attending.add(event)
        context['rsvp_name'] = 'Un-RSVP'
    else:
        profile.attending.remove(event)
    context['form'] = rsvp_form
    context['event'] = event
    return render(request, 'headliner/event.html', context)




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
    if 'event_picture' in request.FILES:
        entry.event_picture = request.FILES['event_picture']

    if not event_form.is_valid():
        context = { 'form': event_form, 'user':user }
        return render(request, 'headliner/global.html', context)
    entry.event_description = event_form.cleaned_data['event_description']
    entry.save()
    posts = Event.objects.all().order_by('-creation_time')

    context = { 'user': user, 'form': event_form, 'entries': posts}
    return render(request, 'headliner/global.html', context)

@login_required
def get_attending(request):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    response_data = {}
    response_data['events'] = []
    user = request.user
    user_profile = get_object_or_404(Profile, user = user)
    events_attending = user_profile.attending.all()
    follower_posts_ids = []
    for event_item in events_attending:
        event_data = {
            'id': event_item.id,
            'title': event_item.title,
            'text': event_item.event_description,
            'location': event_item.location,
            'username': event_item.created_by.username,
            'first_name': event_item.created_by.first_name,
            'last_name': event_item.created_by.last_name,
            'creation_time': event_item.creation_time.isoformat(),
        }
        if event_item.event_picture:
            event_data['picture'] = event_item.event_picture.url
        response_data['events'].append(event_data)

    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')

@login_required
def attending_action(request):
    user = request.user
    user_profile = get_object_or_404(Profile, user = user)
    events_attending = user_profile.attending.all()
    print(events_attending)
    if request.method == 'GET':
        context = {'user': user, 'entries': events_attending}
        return render(request, 'headliner/attending.html', context)
    context = {'user': user, 'entries': events_attending}
    return render(request, 'socialnetwork/attending.html', context)

@login_required
def create_event_action(request):
    user = request.user
    context = {}
    if request.method == 'GET':
        context['form'] = EventForm()
        return render(request, 'headliner/createEvent.html', context)


    entry = Event()
    entry.created_by=request.user
    entry.creation_time=timezone.now()

    event_form = EventForm(request.POST)
    if 'event_picture' in request.FILES:
        entry.event_picture = request.FILES['event_picture']

    if not event_form.is_valid():
        context = { 'form': event_form, 'user':user }
        return render(request, 'headliner/createEvent.html', context)

    entry.event_description = event_form.cleaned_data['event_description']
    entry.title = event_form.cleaned_data['title']
    entry.location = event_form.cleaned_data['location']
    entry.date = event_form.cleaned_data['date']
    entry.price = event_form.cleaned_data['price']

    entry.save()

    context = { 'user': user, 'form': EventForm(), 'status': entry.title + " event has been posted!!" }
    return render(request, 'headliner/createEvent.html', context)



def get_global(request):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    response_data = {}
    response_data['events'] = []
    for event_item in Event.objects.all():
        event_data = {
            'id': event_item.id,
            'title': event_item.title,
            'text': event_item.event_description,
            'location': event_item.location,
            'username': event_item.created_by.username,
            'first_name': event_item.created_by.first_name,
            'last_name': event_item.created_by.last_name,
            'creation_time': event_item.creation_time.isoformat(),
        }
        if event_item.event_picture:
            event_data['picture'] = event_item.event_picture.url
        response_data['events'].append(event_data)

    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')

def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{"error": "' + message + '"}'
    return HttpResponse(response_json, content_type='application/json', status=status)
