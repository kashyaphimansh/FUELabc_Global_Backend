from django.contrib import admin
from django.urls import include, path
from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "api/v1/auth/",
        include("apps.users.urls"),
    ),

    path(
        "api/v1/",
        include("apps.vehicles.urls"),
    ),

    path(
        "api/v1/aem/",
        include("apps.aem.urls"),
    ),

    path("api/v1/tripanalytics/", 
         include("apps.tripanalytics.urls")
         ), 
    path(
        'api/v1/vehicle/',
        include('apps.vehicles.urls'),
    ),
    path(
        'api/v1/payments/',
        include('apps.subscriptions.urls'),
    ),
    path(
        "api/v1/app-settings/",
        include("apps.app_settings.urls"),
    ),

    path("api/v1/co2/",
        include("apps.co2.urls")),

    path("api/v1/mileage-advisor/",
          include("apps.mileage_advisor.urls")),

]
