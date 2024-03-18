from . import views
from django.urls import path
from django.conf import settings

urlpatterns = [
    path('', views.login_action, name="login"),
    path('register/', views.register_action, name="register"),
    path('headliner/get-global', views.get_global, name="get_global"),
    path('create-event/', views.create_event_action, name="create_event"),
    path('global/', views.global_action, name="global"),
    path('event/<int:event_id>/', views.event_action, name="event"),
]