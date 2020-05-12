from django.urls import path

from .views import (
    RunSearch
)

app_name = "search"


urlpatterns = [
    path('', RunSearch.as_view(), name='run_search'),
    path('', EventList.as_view())
   
]
