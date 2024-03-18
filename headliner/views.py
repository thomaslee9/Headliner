# 17-437 Team 30

from django.shortcuts import render
from django.shortcuts import redirect, reverse

from headliner.forms import LoginForm
from headliner.forms import RegisterForm


import json
import datetime
# Create your views here.

def login_action(request):
    context = {}
    if request.user.is_authenticated:
        context['status'] = "User is authenticated."
        return redirect(reverse('global'))
    
    return render(request, 'headliner/login.html', {})