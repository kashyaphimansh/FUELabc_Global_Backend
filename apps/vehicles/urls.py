from django.urls import path
from .views import *

urlpatterns = [

    path(
        'add/',
        VehicleSetupView.as_view()
    ),

    path(
        'list/',
        VehicleListView.as_view()
    ),

    path(
        '<int:pk>/',
        VehicleDetailView.as_view()
    ),

    path(
        'update/<int:pk>/',
        VehicleUpdateView.as_view()
    ),

    path(
        'delete/<int:pk>/',
        VehicleDeleteView.as_view()
    ),

    path('vehicle-makes/', VehicleMakesView.as_view()),

    path('vehicle-models/', VehicleModelsView.as_view()),
]