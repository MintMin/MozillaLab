from django.urls import path

from .views import (
    ViewCalendar,
    TestCalendar,
)

app_name = "calendars"


urlpatterns = [
    path('', ViewCalendar.as_view(), name='view_calendar'),
    path('test/', TestCalendar.as_view(), name='test'),

]
