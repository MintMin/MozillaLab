from django.urls import path

from .views import (
    ViewProfile
)

app_name = "user_profile"


urlpatterns = [
    path('', ViewProfile.as_view(), name='view_profile')
]
