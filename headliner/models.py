# 17-437 Team30
# Headliner App
# models.py

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class Event(models.Model):
    event_description = models.CharField(blank=True, max_length=500, verbose_name='New Event')
    created_by    = models.ForeignKey(User, on_delete=models.PROTECT, related_name="entry_creators")
    creation_time = models.DateTimeField()

    def __str__(self):
        return f"Entry(id={self.id})"


