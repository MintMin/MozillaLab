from django.urls import path
from django.conf.urls import url

from .views import (
    CareerFairDashboard,
    AutocompleteUni,
    CreateBooth,
    detail,
    BoothError

)

app_name = "career_fair"


urlpatterns = [
    path('', CareerFairDashboard.as_view(), name='career_fair_dashboard'),
    url(r'^uni-autocomplete/$', AutocompleteUni.as_view(), name='uni-autocomplete'),
    path('create_booth', CreateBooth.as_view(), name = 'create-booth'),
    url(r'^(?P<event_id>[0-9]+)/$', detail, name='detail'),
    path('error', BoothError.as_view(), name = 'error')
]
