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

class SettingsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        country_code = request.user.country_code
        is_default_country = False

        if not country_code:
            country_code = "AU"
            is_default_country = True

        config = CountryConfig.objects.filter(
            country_code=country_code
        ).first()

        if not config:
            config = CountryConfig.objects.filter(
                country_code="AU"
            ).first()
            is_default_country = True

        return APIResponse.success(
            data={
                "country_code": config.country_code,
                "country_name": config.country_name,
                "is_default_country": is_default_country,
                "currency_code": config.currency_code,
                "currency_symbol": config.currency_symbol,
                "distance_unit": config.distance_unit,
                "fuel_volume_unit": config.fuel_volume_unit,
                "fuel_economy_unit": config.fuel_economy_unit,
                "fuel_types": config.fuel_types,
                "subscription_plans": config.subscription_plans,
                "ev_energy_unit": config.ev_energy_unit,
            }
        )
class TermsAPIView(APIView):
    def get(self, request):
        return Response({
            "title": "Terms & Conditions",
            "last_updated": "July 2026",
            "content": """
    ```

    TERMS & CONDITIONS

    Last Updated: July 2026

    Welcome to FUELabc. By downloading, installing, accessing, or using the FUELabc application ("App"), you agree to be bound by these Terms & Conditions.

    1. ABOUT FUELABC

    FUELabc is developed and operated by Saint Sita Ram Innovation Lab Private Limited ("Company", "we", "our", or "us").

    The App provides fuel cost estimation, mileage optimization assistance, route-related calculations, vehicle information management, and related services.

    2. ELIGIBILITY

    You must be at least 18 years of age or have the consent of a parent or legal guardian to use the App.

    3. SUBSCRIPTION & PURCHASES

    Premium Access – ₹149 (One-Time Purchase for 1 Year)

    This purchase does not automatically renew unless expressly stated at the time of purchase.

    4. MILEAGE & FUEL INFORMATION DISCLAIMER

    Mileage estimates, fuel consumption calculations, route costs, fuel price comparisons, and related information are provided for informational purposes only.

    Actual results may vary based on:
    • Vehicle condition
    • Driving habits
    • Traffic conditions
    • Weather conditions
    • Road conditions
    • Fuel quality
    • Vehicle load and maintenance

    FUELabc does not guarantee the accuracy of any estimate or calculation.

    5. SAFE USE

    You must comply with all traffic laws, vehicle regulations, and manufacturer recommendations while using the App.

    Do not use the App in a manner that distracts you from safe driving.

    You are solely responsible for your driving decisions and vehicle operation.

    6. INTELLECTUAL PROPERTY

    FUELabc, its software, algorithms, content, designs, trademarks, patents, databases, and related intellectual property are owned by Saint Sita Ram Innovation Lab Private Limited.

    7. REFUND POLICY

    Refund requests may be reviewed subject to applicable laws and verification of the circumstances.

    8. LIMITATION OF LIABILITY

    To the maximum extent permitted by law, FUELabc shall not be liable for indirect or consequential damages arising from use of the App.

    9. PRIVACY

    Your use of the App is also governed by our Privacy Policy.

    10. GOVERNING LAW

    These Terms are governed by the laws of India.

    11. CONTACT US

    Saint Sita Ram Innovation Lab Private Limited
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

    PRIVACY POLICY

    Last Updated: July 2026

    Saint Sita Ram Innovation Lab Private Limited ("Company", "we", "our", or "us") operates the FUELabc mobile application ("App").

    This Privacy Policy explains how we collect, use, store, process, and protect your personal information when you use FUELabc.

    INFORMATION WE COLLECT

    We may collect the following information:

    • Username
    • Mobile Number
    • Email Address (Optional)
    • Device Identifier
    • State and District
    • Vehicle Information
    • App Usage Information
    • Location Information (with your permission)

    LOCATION DATA

    FUELabc may collect your device location when permission is granted.

    Location data is used for:

    • Route calculations
    • Journey starting points
    • Map display features
    • Mileage and fuel optimization features

    Location access can be disabled through your device settings, although some features may not function correctly.

    VEHICLE INFORMATION

    We may collect vehicle-related information including:

    • Vehicle Type
    • Manufacturer
    • Model
    • Engine Capacity (CC)
    • Fuel Type

    This information is used to improve mileage calculations, route costs, and fuel estimations.

    HOW WE USE YOUR INFORMATION

    We use your information to:

    • Provide App functionality
    • Verify user accounts
    • Send OTP verification messages
    • Improve App performance
    • Calculate mileage and fuel costs
    • Maintain account security
    • Provide customer support
    • Send important service notifications

    PAYMENT PROCESSING

    Payments may be processed through trusted third-party payment providers such as Razorpay.

    We do not store your complete payment card details on our servers.

    ANALYTICS AND CRASH REPORTING

    We may use analytics services to understand App performance, usage trends, and technical issues.

    Collected analytics information is used solely to improve our services.

    DATA SHARING

    We do not sell personal information.

    Information may be shared only:

    • With payment providers for transaction processing
    • With service providers supporting App operations
    • When required by law
    • To protect legal rights and security

    DATA RETENTION

    We retain information only for as long as necessary to:

    • Provide our services
    • Comply with legal obligations
    • Resolve disputes
    • Enforce agreements

    ACCOUNT DELETION

    Users may request account deletion directly through the App.

    Upon successful verification, personal information associated with the account will be permanently removed unless retention is required by law.

    YOUR RIGHTS

    Depending on your jurisdiction, you may have the right to:

    • Access your personal data
    • Correct inaccurate information
    • Request deletion of data
    • Withdraw consent
    • Request data portability
    • Object to certain processing activities

    Requests may be submitted through support@fuelabc.com.

    DATA SECURITY

    We implement reasonable technical and organizational measures to protect user information.

    Despite these safeguards, no electronic transmission or storage system can be guaranteed to be completely secure.

    CHILDREN'S PRIVACY

    The App is not intended for children under the age of 13.

    We do not knowingly collect personal information from children under 13 years of age.

    INTERNATIONAL USERS

    If you access the App from outside India, your information may be transferred to and processed in India where our systems and service providers operate.

    By using the App, you consent to such transfers where permitted by applicable law.

    INTELLECTUAL PROPERTY

    FUELabc, its software, algorithms, technologies, patents, copyrights, trademarks, and related intellectual property are owned by Saint Sita Ram Innovation Lab Private Limited.

    Unauthorized copying, modification, reverse engineering, distribution, or commercial use is prohibited.

    CHANGES TO THIS PRIVACY POLICY

    We may update this Privacy Policy from time to time.

    Updated versions will be posted within the App and become effective upon publication.

    CONTACT US

    Saint Sita Ram Innovation Lab Private Limited

    Bathinda, Punjab, India

    Email: support@fuelabc.com

    Websites:
    www.fuelabc.com
    www.ssrinnovationlab.com
    """
    })

class CustomerSupportView(APIView):
    permission_classes = [IsAuthenticated]

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