from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from headliner.models import Event
from django.utils import timezone
from headliner.forms import EventForm

# Create your views here.
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