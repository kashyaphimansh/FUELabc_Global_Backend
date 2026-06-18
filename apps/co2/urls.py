from django.urls import path
from .views import CO2TrackingView

app_name = "co2"

urlpatterns = [
    path(
        "tracking/",
        CO2TrackingView.as_view(),
        name="co2-tracking",
    ),
]