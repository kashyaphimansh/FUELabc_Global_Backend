from apps.app_settings.models import CountryConfig
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.responses import APIResponse
from rest_framework.response import Response
from .models import CustomerSupport
from .serializers import CustomerSupportSerializer
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from apps.location.models import Country

class SettingsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        default_country = request.user.country_code or "AU"

        countries = []

        for config in CountryConfig.objects.all().order_by("country_name"):
            location_country = Country.objects.filter(
                iso2=config.country_code
            ).prefetch_related("states").first()

            countries.append({
                "country_code": config.country_code,
                "country_name": config.country_name,
                "is_default": config.country_code == default_country,

                "currency_code": config.currency_code,
                "currency_symbol": config.currency_symbol,

                "distance_unit": config.distance_unit,
                "fuel_volume_unit": config.fuel_volume_unit,
                "fuel_economy_unit": config.fuel_economy_unit,
                "ev_price_unit": config.ev_price_unit,
                "ev_efficiency_unit": config.ev_efficiency_unit,

                "fuel_price_min": config.fuel_price_min,
                "fuel_price_max": config.fuel_price_max,

                "ev_price_min": config.ev_price_min,
                "ev_price_max": config.ev_price_max,

                "fuel_efficiency_min": config.fuel_efficiency_min,
                "fuel_efficiency_max": config.fuel_efficiency_max,

                "ev_efficiency_min": config.ev_efficiency_min,
                "ev_efficiency_max": config.ev_efficiency_max,

                "speed_min": config.speed_min,
                "speed_max": config.speed_max,

                "yearly_distance_min": config.yearly_distance_min,
                "yearly_distance_max": config.yearly_distance_max,
                "fuel_types": config.fuel_types,
                "subscription_plans": config.subscription_plans,

                "location_country_id": (
                    location_country.id if location_country else None
                ),

                "states": [
                    {
                        "id": state.id,
                        "name": state.name,
                    }
                    for state in (
                        location_country.states.all()
                        if location_country and config.country_code == default_country
                        else []
                    )
                ],
            })

        return APIResponse.success(
            data={
                "default_country": default_country,
                "countries": countries,
            }
        )

class CityListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        state_id = request.GET.get("state_id")

        cities = City.objects.filter(
            state_id=state_id
        ).order_by("name")

        return APIResponse.success(
            data=[
                {
                    "id": city.id,
                    "name": city.name,
                }
                for city in cities
            ]
        )
                
class TermsAPIView(APIView):
    def get(self, request):
        return Response({
            "title": "Terms & Conditions",
            "last_updated": "July 2026",
            "content": """
# Terms & Conditions

**Last Updated:** July 2026

Welcome to **FUELabc**.

These Terms & Conditions ("Terms") govern your access to and use of the FUELabc mobile application ("App"). By downloading, installing, or using the App, you agree to these Terms.

---

## 1. About FUELabc

FUELabc is owned and operated by **Saint Sita Ram Innovation Lab Private Limited**.

The App provides features including:

- Fuel cost estimation
- Mileage calculations
- EV charging cost estimation
- Vehicle management
- Trip and route calculations
- Fuel price comparison
- Related vehicle utilities

---

## 2. Eligibility

You must be at least **18 years old**, or have permission from a parent or legal guardian to use the App.

---

## 3. User Account

You are responsible for:

- Keeping your account secure
- Providing accurate information
- Maintaining your login credentials

You must immediately notify us of any unauthorized access.

---

## 4. Subscription & Purchases

Some features require a paid subscription or one-time purchase.

Unless otherwise stated:

- Prices are displayed within the App.
- Payments are processed through authorized payment providers.
- Refunds are subject to Google Play Store, Apple App Store, or applicable consumer laws.

---

## 5. Fuel Prices & Mileage Disclaimer

FUELabc provides estimated calculations only.

Actual fuel costs, mileage, EV efficiency, and travel expenses may vary depending on:

- Driving style
- Traffic
- Weather
- Road conditions
- Vehicle maintenance
- Vehicle load
- Fuel quality
- Battery condition (EV)

We do not guarantee the accuracy of any estimate.

---

## 6. Safe Driving

Never operate the App in a way that distracts you while driving.

You are solely responsible for complying with all road rules and traffic laws applicable in your country.

---

## 7. Intellectual Property

All content, software, algorithms, trademarks, logos, graphics, and intellectual property within FUELabc remain the exclusive property of Saint Sita Ram Innovation Lab Private Limited.

No part of the App may be copied, modified, reverse engineered, distributed, or commercially exploited without written permission.

---

## 8. Limitation of Liability

To the maximum extent permitted by law, FUELabc is not liable for:

- Indirect damages
- Loss of profits
- Loss of data
- Vehicle damage
- Fuel expenses
- Travel costs
- Business interruption

Use of the App is entirely at your own risk.

---

## 9. Third-Party Services

The App may integrate with third-party services including:

- Google Maps
- Payment providers
- Analytics providers
- Cloud services

These services have their own privacy policies and terms.

---

## 10. Privacy

Your use of the App is also governed by our Privacy Policy.

---

## 11. Changes to these Terms

We may update these Terms from time to time.

Continued use of the App after updates means you accept the revised Terms.

---

## 12. Governing Law

If you use the App in Australia or New Zealand, these Terms are subject to applicable consumer protection and privacy laws in your jurisdiction.

Other users remain subject to the laws applicable in their country where required.

---

## 13. Contact Us

**Saint Sita Ram Innovation Lab Private Limited**

Bathinda, Punjab, India

Email: [support@fuelabc.com](mailto:support@fuelabc.com)

Websites:
[www.fuelabc.com](http://www.fuelabc.com)
[www.ssrinnovationlab.com](http://www.ssrinnovationlab.com)
"""
    })

class PrivacyPolicyAPIView(APIView):

    def get(self, request):
        return Response({
            "title": "Privacy Policy",
            "last_updated": "July 2026",
            "content": """
# Privacy Policy

**Last Updated:** July 2026

FUELabc ("we", "our", or "us") respects your privacy.

This Privacy Policy explains how we collect, use, store, and protect your personal information.

---

## Information We Collect

Depending on how you use the App, we may collect:

- Name
- Mobile number
- Email address
- Country
- State
- City
- Device information
- Vehicle information
- Usage analytics
- Location (only with your permission)

---

## Location Information

If permission is granted, we may access your device location for:

- Navigation
- Route calculations
- Fuel cost estimation
- Nearby fuel stations
- Trip management

You may disable location access at any time through your device settings.

---

## Vehicle Information

We may collect:

- Vehicle type
- Manufacturer
- Model
- Fuel type
- Engine capacity
- EV battery information (where applicable)

This information helps improve mileage and fuel cost calculations.

---

## How We Use Your Information

We use your information to:

- Create and manage your account
- Verify your identity
- Improve App functionality
- Calculate fuel costs
- Calculate EV charging costs
- Improve mileage estimates
- Respond to support requests
- Detect fraud
- Send important service notifications

---

## Payments

Payments may be processed through trusted third-party payment providers.

We do not store your complete debit or credit card details.

---

## Analytics

We may use trusted analytics providers to:

- Monitor crashes
- Improve performance
- Understand feature usage
- Enhance user experience

Analytics data is generally aggregated and anonymized where practical.

---

## Information Sharing

We do **not sell** your personal information.

We may share information only with:

- Payment providers
- Cloud service providers
- Analytics providers
- Legal authorities where required by law

---

## Data Security

We implement reasonable administrative, technical, and physical safeguards to protect your information.

However, no online service can guarantee complete security.

---

## Data Retention

We retain personal information only as long as necessary to:

- Provide our services
- Meet legal obligations
- Resolve disputes
- Enforce agreements

---

## Your Rights

Depending on your location, you may have rights to:

- Access your personal information
- Correct inaccurate information
- Request deletion
- Withdraw consent
- Request data portability
- Object to certain processing

Requests can be sent to:

**support@fuelabc.com**

---

## Australia

If you are located in Australia, we handle personal information in accordance with the **Privacy Act 1988 (Cth)** and the **Australian Privacy Principles (APPs)**.

---

## New Zealand

If you are located in New Zealand, personal information is handled in accordance with the **Privacy Act 2020 (NZ)**.

---

## Children's Privacy

FUELabc is not intended for children under 13 years of age.

We do not knowingly collect personal information from children.

---

## International Data Transfers

Your information may be stored and processed on servers located in different countries where our service providers operate.

By using the App, you consent to such transfers where permitted by applicable law.

---

## Changes to this Privacy Policy

We may update this Privacy Policy from time to time.

The latest version will always be available within the App.

---

## Contact Us

**Saint Sita Ram Innovation Lab Private Limited**

Bathinda, Punjab, India

Email: support@fuelabc.com

Websites:
www.fuelabc.com
www.ssrinnovationlab.com
"""
    })

class CustomerSupportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = CustomerSupport.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = CustomerSupportSerializer(
            tickets,
            many=True,
        )

        return Response({
            "success": True,
            "data": serializer.data,
        })

    def post(self, request):
        serializer = CustomerSupportSerializer(data=request.data)

        if serializer.is_valid():

            support_request = CustomerSupport.objects.create(
                user=request.user,
                message=serializer.validated_data["message"],
            )

            try:
                send_mail(
                    subject="New Customer Support Request",
                    message=f"""
User Name: {request.user.name}
User Email: {request.user.email}

Message:
{support_request.message}
""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=["support@fuelabc.com"],
                    fail_silently=False,
                )
            except Exception as e:
                print("EMAIL ERROR:", e)

            return Response(
                {
                    "success": True,
                    "message": "Support request submitted successfully."
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )