# 17-437 Team 30

from django.shortcuts import render
from django.shortcuts import redirect, reverse

from headliner.forms import LoginForm
from headliner.forms import RegisterForm

from django.contrib.auth.decorators import login_required
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
    
    return render(request, 'headliner/login.html', {})

@login_required
def global_action(request):
    user = request.user
    if request.method == 'GET':
        p = EventForm()
        posts = Event.objects.all().order_by('-creation_time')
        context = {'user': user, 'form': p, 'entries': posts}
        return render(request, 'headliner/global.html', context)

    entry = Event()
    entry.created_by=request.user
    entry.creation_time=timezone.now()

    post_form = EventForm(request.POST)
    if not post_form.is_valid():
        context = { 'form': post_form, 'user':user }
        return render(request, 'headliner/global.html', context)
    
    entry.post_input_text = post_form.cleaned_data['post_input_text']
    entry.save()
    posts = Event.objects.all().order_by('-creation_time')
    context = { 'user': user, 'form': post_form, 'entries': posts}
    return render(request, 'headliner/global.html', context)

