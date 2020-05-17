from django.urls import path

from .views import (
    ViewEvent,
    ExampleEvent
)

app_name = "event"


urlpatterns = [
    path('', ViewEvent.as_view(), name='view_event'),
    path('example_event', ExampleEvent.as_view(), name='example_event'),
]
