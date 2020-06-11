from django.urls import path
from django.conf.urls import url, include

from .views import (
    ViewEvent,
    EventList,
    MyEventList,
    CreateEvent,
    EventDashboard,
    detail,
    rsvp,
    un_rsvp,
    delete_event,
    PastEventList
    )

app_name = "event"


urlpatterns = [
    path('', EventDashboard.as_view(), name='event_dashboard'),
    path('event_list/', EventList.as_view(), name='event_list'),
    path('my_event_list/', MyEventList.as_view(), name='my_event_list'),
    url(r'^rsvp/(?P<event_id>[0-9]+)/$', rsvp, name='rsvp'),
    url(r'^un_rsvp/(?P<event_id>[0-9]+)/$', un_rsvp, name='un_rsvp'),
    url(r'^delete_event/(?P<event_id>[0-9]+)/$', delete_event, name='delete_event'),
    path('create_event', CreateEvent.as_view(), name ='create_event'),
    url(r'^(?P<event_id>[0-9]+)/$', detail, name='detail'),
    path('past_event/', PastEventList.as_view(), name='past_event'),
]
