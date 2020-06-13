from django.urls import path
from django.conf.urls import url

from .views import (
    CareerFairDashboard,
    AutocompleteUni,
    CreateBooth,
    detail,
    BoothError,
    booth_detail,
    signup,
    remove,
    change
)

app_name = "career_fair"


urlpatterns = [
    path('', CareerFairDashboard.as_view(), name='career_fair_dashboard'),
    url(r'^uni-autocomplete/$', AutocompleteUni.as_view(), name='uni-autocomplete'),
    path('create_booth', CreateBooth.as_view(), name = 'create-booth'),
    url(r'^(?P<event_id>[0-9]+)/$', detail, name='detail'),
    path('error', BoothError.as_view(), name = 'error'),
    url(r'^(?P<event_id>[0-9]+)/details/(?P<booth_company>[\w\-]+)/$', booth_detail, name='booth_detail'),
    url(r'^signup/(?P<slot_id>[0-9]+)/$', signup, name='signup'),
    url(r'^remove/(?P<slot_id>[0-9]+)/$', remove, name='remove'),
    url(r'^change/(?P<slot_id>[0-9]+)/$', change, name='change'),
]
