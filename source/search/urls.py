from django.urls import path

from .views import (
    # RunSearch,
    run_search,
    # filters,

)

app_name = "search"


urlpatterns = [
    # path('', RunSearch.as_view(), name='run_search'),
    path('', run_search, name='run_search'),
    # path('', filters, name='filters'),
]
