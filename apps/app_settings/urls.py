from django.urls import path

from .views import SettingsView, TermsAPIView, PrivacyPolicyAPIView, CustomerSupportView, CityListAPIView

urlpatterns = [

    path(
        "settings/",
        SettingsView.as_view(),
    ),

    path(
        "getCity/",
        CityListAPIView.as_view(),
    ),

    path(
        "terms/",
        TermsAPIView.as_view(),
    ),

    path(
        "privacy/",
        PrivacyPolicyAPIView.as_view(),
    ),

    path(
        "customer-support/",
        CustomerSupportView.as_view(),
    ),
]