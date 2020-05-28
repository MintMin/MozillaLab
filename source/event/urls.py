from django.urls import path
from django.conf.urls import url, include

from .views import (
    ViewEvent,
    ExampleEvent,
    CreateEvent,
    EventDashboard,
    detail,
    rsvp
    )

app_name = "event"


urlpatterns = [
    path('', EventDashboard.as_view(), name='event_dashboard'),
    # path('rsvp', rsvp, name = 'rsvp'),
    url(r'^rsvp/(?P<event_id>[0-9]+)/$', rsvp, name='rsvp'),
    path('example_event', ExampleEvent.as_view(), name='example_event'),
    path('create_event', CreateEvent.as_view(), name ='create_event'),
    url(r'^(?P<event_id>[0-9]+)/$', detail, name='detail'),
]
