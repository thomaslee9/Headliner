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
    location = models.CharField(max_length=100, verbose_name='Location', null=True)
    date = models.DateField(verbose_name='Date', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="entry_creators", verbose_name='Created By')
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='Creation Time')

    def __str__(self):
        return f"Entry( id={self.id}, {self.title} ) created by {self.created_by}"