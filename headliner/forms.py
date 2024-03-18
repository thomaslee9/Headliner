from django import forms
from headliner.models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_description']