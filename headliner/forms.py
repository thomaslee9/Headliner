# 17-437 Team30
# Headliner App
# forms.py


from django import forms

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from headliner.models import Event


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", required=True, max_length=20)
    password = forms.CharField(label="Password", required=True, max_length=200, widget=forms.PasswordInput())

    def clean(self):
        # Clean Parent
        cleaned_data = super().clean()

        # Authenticate
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("Invalid username or password please try again")
        
        # Return Cleaned Data
        return cleaned_data
    

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', required=True, max_length=20)
    password = forms.CharField(label='Password', required=True, max_length=200, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm', required=True, max_length=200, widget=forms.PasswordInput())
    email = forms.CharField(label='E-mail', required=True, max_length=100)
    first_name = forms.CharField(label='First Name', required=True, max_length=100)
    last_name = forms.CharField(label='Last Name', required=True, max_length=100)

    def clean(self):
        # Clean Parent
        cleaned_data = super().clean()
        # Parse password field inputs
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        # Check confirmation password 
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords did not match.")
        
        # Return Cleaned Data
        return cleaned_data
    
    def clean_username(self):
        # Parse username field input
        username = self.cleaned_data.get('username')
        # Check if username is already taken 
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken. Please choose another.")

        # Return Cleaned Data
        return username

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_description', 'event_picture']

