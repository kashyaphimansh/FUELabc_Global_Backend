from django.urls import path
from .views import *

urlpatterns = [

    path(
        'vehicle/add/',
        VehicleSetupView.as_view()
    ),

    path(
        'vehicle/list/',
        VehicleListView.as_view()
    ),

    path(
        'vehicle/<int:pk>/',
        VehicleDetailView.as_view()
    ),

    path(
        'vehicle/<int:pk>/update/',
        VehicleUpdateView.as_view()
    ),

    path(
        'vehicle/<int:pk>/delete/',
        VehicleDeleteView.as_view()
    ),
]