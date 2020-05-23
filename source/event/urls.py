from django.urls import path

from .views import (
    ViewEvent,
    ExampleEvent,
    CreateEvent
)

app_name = "event"


urlpatterns = [
    path('', ViewEvent.as_view(), name='view_event'),
    path('example_event', ExampleEvent.as_view(), name='example_event'),
    path('create_event', CreateEvent.as_view(), name ='create_event'),
]
