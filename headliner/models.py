# 17-437 Team30
# Headliner App
# models.py

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class Event(models.Model):

    event_picture = models.ImageField(upload_to='event_pictures/', null=True, blank=True, verbose_name='Add a Photo')
    event_description = models.TextField(blank=True, verbose_name='Description')
    title = models.CharField(max_length=100, verbose_name='Title', null=True)
    location = models.CharField(max_length=300, verbose_name='Location', null=True)
    date = models.DateField(verbose_name='Date', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="entry_creators", verbose_name='Created By')
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='Creation Time')
    groups = models.ManyToManyField('EventGroup', related_name='groups')

    def __str__(self):
        return f"Event(id={self.id})"

class EventGroup(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    messages = models.ManyToManyField('Message', related_name='messages')

    def __str__(self):
        return f"EventGroup(id={self.id})"

class Profile(models.Model):
    prof_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, verbose_name='Add a Photo')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    content_type = models.CharField(blank=True, max_length=50)

    attending = models.ManyToManyField(Event, related_name='attending')
    my_events = models.ManyToManyField(Event, related_name='my_events')

    def __str__(self):
        return f"Profile(id={self.id})"


class Message(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="post_creators")
    text = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True, verbose_name='Add a Photo')
    event = models.ForeignKey(Event, default=None, on_delete=models.PROTECT)


    def __str__(self):
        return f"Profile(id={self.id})"
