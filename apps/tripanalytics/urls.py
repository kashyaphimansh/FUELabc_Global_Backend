"""
Trip Analytics URLs
"""

from django.urls import path
from .views import TripHistoryView

app_name = "tripanalytics"

urlpatterns = [
    path(
        "history/",
        TripHistoryView.as_view(),
        name="trip-history",
    ),
]