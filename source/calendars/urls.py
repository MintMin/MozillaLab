from django.urls import path

from .views import (
    ViewCalendar
)

app_name = "calendars"


urlpatterns = [
    path('', ViewCalendar.as_view(), name='view_calendar')
]
