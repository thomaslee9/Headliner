# 17-437 Team30
# Headliner App
# views.py

from django.shortcuts import render
from django.shortcuts import redirect , get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, Http404

from headliner.forms import LoginForm
from headliner.forms import RegisterForm, RSVPForm, MyProfileForm, CreateGroupForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from headliner.models import Event, Profile, Message, ChatGroup
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
def get_pfp(request, user_id):
    profile = get_object_or_404(Profile, id=user_id)

    if not profile.prof_picture:
        raise Http404

    return HttpResponse(profile.prof_picture)


@login_required
def event_action(request, event_id):
    context = {}
    event = get_object_or_404(Event, id=event_id)
    context['event'] = event
    context['rsvp_name'] = 'RSVP'
    context['userID'] = request.user.id
    context['chat_groups'] = event.groups.all()
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
        return render(request, 'headliner/event.html', context)
    is_attending = profile.attending.filter(id=event.id).exists()

    if request.method == 'GET':
        rsvp_form = RSVPForm()
        groupcreation_form = CreateGroupForm()
        context['form'] = rsvp_form
        context['createGroup_form'] = groupcreation_form
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

    createGroup_form = CreateGroupForm(request.POST)
    if not createGroup_form.is_valid():
        context = { 'createGroup_form': createGroup_form, 'event':event, 'form': rsvp_form }
        return render(request, 'headliner/event.html', context)
    else:
        if 'create_group_button' in request.POST:
            group_name = createGroup_form.cleaned_data['name']
            new_group = ChatGroup.objects.create(name=group_name, event=event)
            event.groups.add(new_group)

    context['form'] = rsvp_form
    context['createGroup_form'] = createGroup_form
    context['event'] = event
    context['chat_groups'] = event.groups.all()
    return render(request, 'headliner/event.html', context)

@login_required
def event_chat_action(request, event_id, chat_id):
    context = {}
    event = get_object_or_404(Event, id=event_id)
    context['event'] = event
    context['rsvp_name'] = 'RSVP'
    context['userID'] = request.user.id
    context['chat_groups'] = event.groups.all()
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None
        return render(request, 'headliner/event.html', context)
    is_attending = profile.attending.filter(id=event.id).exists()

    if request.method == 'GET':
        rsvp_form = RSVPForm()
        groupcreation_form = CreateGroupForm()
        context['form'] = rsvp_form
        context['createGroup_form'] = groupcreation_form
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

    createGroup_form = CreateGroupForm(request.POST)
    if not createGroup_form.is_valid():
        context = { 'createGroup_form': createGroup_form, 'event':event, 'form': rsvp_form }
        return render(request, 'headliner/event.html', context)
    else:
        if 'create_group_button' in request.POST:
            group_name = createGroup_form.cleaned_data['name']
            new_group = ChatGroup.objects.create(name=group_name, event=event)
            event.groups.add(new_group)

    context['form'] = rsvp_form
    context['createGroup_form'] = createGroup_form
    context['event'] = event
    context['chat_groups'] = event.groups.all()
    return render(request, 'headliner/event.html', context)


@login_required
def myprofile_action(request):
    context = {}
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        context = {
            'form': MyProfileForm(initial={'bio': request.user.profile.bio})
        }
        return render(request, 'headliner/myprofile.html', context)

    form = MyProfileForm(request.POST, request.FILES)

    if not form.is_valid():
        context['form'] = form
        return render(request, 'headliner/myprofile.html', context)

    profile.bio = form.cleaned_data['bio']
    profile.prof_picture = form.cleaned_data['prof_picture']
    profile.content_type = form.cleaned_data['prof_picture'].content_type
    profile.save()

    context['status'] = "Your Profile has been Updated Successfully."

    context['form'] = MyProfileForm(initial={'bio': request.user.profile.bio})

    return render(request, 'headliner/myprofile.html', context)


@login_required
def otherprofile_action(request, user_id):
    context = {}
    profile = get_object_or_404(Profile, id=user_id)
    context['profile'] = profile
    return render(request, 'headliner/otherprofile.html', context)


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
    response_data['user_id'] = user_profile.id

    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')

@login_required
def attending_action(request):
    user = request.user
    user_profile = get_object_or_404(Profile, user = user)
    events_attending = user_profile.attending.all()
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

    chat_group = ChatGroup.objects.create(name="Global", event=entry)
    entry.groups.add(chat_group)
    entry.save()

    context = { 'user': user, 'form': EventForm(), 'status': entry.title + " event has been posted!!" }
    return render(request, 'headliner/createEvent.html', context)



@login_required
def edit_event_action(request, event_id):
    user = request.user
    context = {}
    event = get_object_or_404(Event, id=event_id)
    context['event'] = event

    if request.method == 'GET':
        context['form'] = EventForm(instance=event)
        return render(request, 'headliner/editEvent.html', context)
    
    # event.created_by=user
    # event.creation_time=timezone.now()

    event_form = EventForm(request.POST)
    if 'event_picture' in request.FILES:
        event.event_picture = request.FILES['event_picture']

    if not event_form.is_valid():
        context = { 'form': event_form, 'user':user }
        return render(request, 'headliner/createEvent.html', context)

    event.event_description = event_form.cleaned_data['event_description']
    event.title = event_form.cleaned_data['title']
    event.location = event_form.cleaned_data['location']
    event.date = event_form.cleaned_data['date']
    event.price = event_form.cleaned_data['price']
    event.save()

    context = { 'user': user, 'form': event_form, 'status': event.title + " event has been updated!!", 'event': event }

    return render(request, 'headliner/event.html', context)


def get_global(request):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    response_data = {}
    response_data['events'] = []
    for event_item in Event.objects.all():
        event_data = {
            'id': event_item.id,
            'userID': event_item.created_by.id,
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
    response_data['user_id'] = request.user.id

    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')

def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{"error": "' + message + '"}'
    return HttpResponse(response_json, content_type='application/json', status=status)


def add_message(request):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not 'message_text' in request.POST or not request.POST['message_text']:
        return _my_json_error_response("You must enter a Chat Message to add.", status=400)

    if not 'event_id' in request.POST or not request.POST['event_id'] or not request.POST['event_id'].isdigit():
        return _my_json_error_response("Comment must be added to an Event.", status=400)


    if not 'chat_id' in request.POST or not request.POST['chat_id'] or not request.POST['chat_id'].isdigit():
        return _my_json_error_response("Comment must be added to an Event.", status=400)

    try:
        event_id = int(request.POST['event_id'])
    except:
        return _my_json_error_response("Comment must be added to an Event (with int event_id).", status=400)

    try:
        chat_id = int(request.POST['chat_id'])
    except:
        return _my_json_error_response("Comment must be added to an Event (with int chat_id).", status=400)

    # Build Message
    new_chat = Message()
    new_chat.created_by = request.user

    timeString = timezone.localtime()
    new_chat.creation_time = str(timeString.strftime('%-m/%-d/%Y %-I:%M %p'))

    new_chat.text = request.POST['message_text']

    try:
        new_chat.event = Event.objects.get(id=event_id)
    except:
        return _my_json_error_response("Comment needs an existing Event.", status=400)

    new_chat.save()

    chatGroup = get_object_or_404(ChatGroup, id=chat_id)
    chatGroup.messages.add(new_chat)
    return get_new_chat(request)


def get_new_chat(request):
    response_data = []

    newChat = Message.objects.all().last()

    if newChat:
        item = {
            'id': newChat.id,
            'text': newChat.text,
            'created_by': newChat.created_by.id,
            'username': newChat.created_by.username,
            'creation_time': newChat.creation_time,
            'event_id': newChat.event.id,
        }

        if newChat.created_by.profile.prof_picture:
            item['picture'] = newChat.created_by.profile.prof_picture.url
        response_data.append(item)

    response_json = json.dumps(response_data)

    return HttpResponse(response_json, content_type='application/json')


def get_event(request, event_id):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    try:
        curr_event = Event.objects.get(id=event_id)
    except:
        return _my_json_error_response("Comment needs an existing Event.", status=400)

    chat_groups = curr_event.groups.all()

    response_data = {}

    # Collect all Messages
    for group_item in chat_groups:
        response_data[str(group_item.id)] = []
        for model_item in group_item.messages.all():
            my_item = {
                'group_name': group_item.name,
                'group_id': group_item.id,
                'id': model_item.id,
                'text': model_item.text,
                'created_by': model_item.created_by.id,
                'username': model_item.created_by.username,
                'creation_time': model_item.creation_time,
                'event_id': model_item.event.id,
            }

            if model_item.created_by.profile.prof_picture:
                my_item['picture'] = model_item.created_by.profile.prof_picture.url
            response_data[str(group_item.id)].append(my_item)
    response_json = json.dumps(response_data)

    return HttpResponse(response_json, content_type='application/json')
