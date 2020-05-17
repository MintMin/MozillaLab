from django.urls import path

from .views import (
    ViewEvent
)

app_name = "event"


urlpatterns = [
    path('', ViewEvent.as_view(), name='view_event'),

]
