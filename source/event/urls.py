from django.urls import path
from django.conf.urls import url, include

from .views import (
    ViewEvent,
    EventList,
    MyEventList,
    CreateEvent,
    EventDashboard,
    detail,
    rsvp
    )

app_name = "event"


urlpatterns = [
    path('', EventDashboard.as_view(), name='event_dashboard'),
    path('event_list/', EventList.as_view(), name='event_list'),
    path('my_event_list/', MyEventList.as_view(), name='my_event_list'),
    url(r'^rsvp/(?P<event_id>[0-9]+)/$', rsvp, name='rsvp'),
    path('create_event', CreateEvent.as_view(), name ='create_event'),
    url(r'^(?P<event_id>[0-9]+)/$', detail, name='detail'),
]
