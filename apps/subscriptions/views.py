from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
import razorpay
from .models import (
    UserSubscription,
    Payment,
)
from apps.app_settings.models import CountryConfig

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        plan_code = request.data.get("plan")
        print("PLAN RECEIVED =", plan_code)

        country_code = request.user.country_code or "AU"

        country_config = CountryConfig.objects.filter(
            country_code=country_code
        ).first()

        if not country_config:
            country_config = CountryConfig.objects.get(country_code="AU")

        plans = country_config.subscription_plans

        active_subscription = UserSubscription.objects.filter(
            user=request.user,
            status="active",
            expires_at__gt=timezone.now(),
        ).exists()

        if active_subscription:
            return Response(
                {
                    "error": "You already have an active subscription"
                },
                status=400,
            )

        country_code = request.user.country_code or "AU"

        country_config = CountryConfig.objects.filter(
            country_code=country_code
        ).first()

        if not country_config:
            country_config = CountryConfig.objects.get(
                country_code="AU"
            )

        plans = country_config.subscription_plans

        if plan_code == "premium_monthly":
            amount = plans["premium"]["monthly_price"]
            duration_days = plans["premium"]["monthly_duration_days"]

        elif plan_code == "premium_yearly":
            amount = plans["premium"]["yearly_price"]
            duration_days = plans["premium"]["yearly_duration_days"]

        elif plan_code == "basic":
            amount = plans["basic"]["price"]
            duration_days = 0

        else:
            return Response(
                {
                    "success": False,
                    "error": "Invalid plan"
                },
                status=400,
            )

        amount_paise = int(float(amount) * 100)

        currency = country_config.currency_code

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET,
            )
        )

        try:
            order = client.order.create({
                "amount": amount_paise,
                "currency": currency,
                "payment_capture": 1,
            })
        except Exception as e:
            import traceback

            traceback.print_exc()

            print("RAZORPAY ERROR =", repr(e))

            return Response({
                "success": False,
                "error": str(e),
            }, status=400)

        UserSubscription.objects.filter(
            user=request.user,
            status="pending",
        ).delete()

        subscription = UserSubscription.objects.create(
            user=request.user,
            plan_code=plan_code,
            amount=amount,
            currency=currency,
            duration_days=duration_days,
            status="pending",
        )

        Payment.objects.create(
            user=request.user,
            subscription=subscription,
            razorpay_order_id=order["id"],
            amount=amount,
            currency=currency,
            status="created",
        )

        return Response({
            "success": True,
            "order_id": order["id"],
            "amount": amount_paise,
            "currency": currency,
            "display_amount": amount,
        })

class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        payment_id = request.data.get(
            "payment_id"
        )

        order_id = request.data.get(
            "order_id"
        )

        signature = request.data.get(
            "signature"
        )

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET,
            )
        )

        try:

            client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            })

            payment = Payment.objects.get(
                razorpay_order_id=order_id,
                user=request.user,
            )

            if payment.status == "paid":
                return Response({
                    "success": True,
                    "message": "Payment already verified"
                })

            razorpay_payment = client.payment.fetch(
                payment_id
            )

            expected_amount = int(
                payment.amount * 100
            )

            if razorpay_payment["amount"] != expected_amount:
                return Response(
                    {
                        "success": False,
                        "error": "Amount mismatch"
                    },
                    status=400,
                )

            payment.status = "paid"
            payment.razorpay_payment_id = payment_id
            payment.save()

            subscription = payment.subscription

            subscription.status = "active"
            subscription.starts_at = timezone.now()

            subscription.expires_at = timezone.now() + timedelta(
                days=subscription.duration_days
            )

            subscription.save()
            
            user = request.user

            user.is_premium = True

            user.subscription_plan = subscription.plan_code

            user.subscription_expires_at = (
                subscription.expires_at
            )
            user.trips_used = 0

            user.save(
                update_fields=[
                    "is_premium",
                    "subscription_plan",
                    "subscription_expires_at",
                    "trips_used"
                ]
            )

            return Response({
                "success": True
            })

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "error": str(e),
                },
                status=400,
            )