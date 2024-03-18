# 17-437 Team30
# Headliner App
# views.py

from django.shortcuts import render
from django.shortcuts import redirect, reverse

from headliner.forms import LoginForm
from headliner.forms import RegisterForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from headliner.models import Event
from django.utils import timezone
from headliner.forms import EventForm

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
        context = {'status': "Log-in to Headliner"}
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
    
    return redirect(reverse('global'))


def register_action(request):
    context = {}
    # Register to Headiner
    if request.method == 'GET':
        context = {'status': "Social Network Registration"}
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

    return redirect(reverse('global'))



@login_required
def global_action(request):
    user = request.user
    if request.method == 'GET':
        p = EventForm()
        events = Event.objects.all().order_by('-creation_time')
        context = {'user': user, 'form': p, 'entries': events}
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

    # context = { 'user': user, 'form': post_form, 'entries': posts}
    # return render(request, 'headliner/global.html', context)

