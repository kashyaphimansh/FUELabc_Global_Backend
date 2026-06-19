from django.urls import path
from .views import MileageAdvisorView

urlpatterns = [
    path("driving-profile/<int:vehicle_id>/", MileageAdvisorView.as_view()),
]