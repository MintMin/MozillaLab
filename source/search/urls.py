from django.urls import path

from .views import (
    RunSearch,
    EventView
)

app_name = "search"


urlpatterns = [
    path('', RunSearch.as_view(), name='run_search'),
    path('student_event/', EventView.as_view(), name='student_event'),
]
