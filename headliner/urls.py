from . import views
from django.urls import path
from django.conf import settings

urlpatterns = [
    path('', views.login_action, name="login"),
    path('register/', views.register_action, name="register"),
    path('global/', views.global_action, name="global"),
]