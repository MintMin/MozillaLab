from django.urls import path

from .views import (
    CareerFairDashboard
)

app_name = "career_fair"


urlpatterns = [
    path('', CareerFairDashboard.as_view(), name='career_fair_dashboard'),
]
