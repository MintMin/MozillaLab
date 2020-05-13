from django.urls import path

from .views import (
    ViewInfosession
)

app_name = "infosession"


urlpatterns = [
    path('', ViewInfosession.as_view(), name='view_infosession')
]
