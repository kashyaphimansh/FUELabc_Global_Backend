from django.urls import path
from .views import TripHistoryView, TripSaveView

app_name = "tripanalytics"

urlpatterns = [
    path(
        "history/",
        TripHistoryView.as_view(),
    ),

    path(
        "save/",
        TripSaveView.as_view(),
    ),
]