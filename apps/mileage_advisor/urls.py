from django.urls import path

from .views import DrivingProfileView

urlpatterns = [
    path("driving-profile/", DrivingProfileView.as_view()),
]