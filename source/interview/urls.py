from django.urls import path

from .views import (
    ViewInterview
)

app_name = "interview"


urlpatterns = [
    path('', ViewInterview.as_view(), name='view_interview')
]
