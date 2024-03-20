from . import views
from django.urls import path
from django.conf import settings

urlpatterns = [
    path('', views.login_action, name="login"),
    path('register/', views.register_action, name="register"),
    path('log-in', views.login_action, name="login"),
    path('logout', views.logout_action, name="logout"),
    path('headliner/get-global', views.get_global, name="get_global"),
    path('headliner/get-attending', views.get_attending, name="get_attending"),
    path('create-event/', views.create_event_action, name="create_event"),
    path('global/', views.global_action, name="global"),
    path('attending/', views.attending_action, name="attending"),

    path('event/<int:event_id>/', views.event_action, name="event"),
    path('photo/<int:event_id>/', views.get_photo, name="photo")
]