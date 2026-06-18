"""
CO2 Tracking API Views

GET /api/v1/co2/tracking/

USA/Canada format:
- Distance : km + miles
- CO2      : grams + lbs (1g = 0.00220462 lbs)
"""

import logging
from datetime import datetime, timedelta

import pytz
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tripanalytics.models import Trip
from .models import CO2Equivalent

logger = logging.getLogger(__name__)

# ==========================================================
# Unit helpers
# ==========================================================

KM_TO_MILES    = 0.621371
GRAMS_TO_LBS   = 0.00220462
KG_TO_LBS      = 2.20462


def _g_to_lbs(grams):
    return round(grams * GRAMS_TO_LBS, 4)


def _kg_to_lbs(kg):
    return round(kg * KG_TO_LBS, 4)


def _km_to_miles(km):
    return round(km * KM_TO_MILES, 2)


# ==========================================================
# View
# ==========================================================

class CO2TrackingView(APIView):
    """
    GET /api/v1/co2/tracking/

    Query Parameters:
        period     : today | yesterday | this_week | last_week | this_month | all_time | custom
        start_date : YYYY-MM-DD (required if period=custom)
        end_date   : YYYY-MM-DD (required if period=custom)
        page       : int (default 1)
        page_size  : int (default 10, max 50)
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            period_type = request.GET.get("period", "this_week")
            start_date  = request.GET.get("start_date")
            end_date    = request.GET.get("end_date")
            page        = int(request.GET.get("page", 1))
            page_size   = min(int(request.GET.get("page_size", 10)), 50)

            current_start, current_end = self._get_date_range(period_type, start_date, end_date)
            prev_start, prev_end       = self._get_previous_period(period_type, current_start, current_end)

            current_trips  = self._get_trips(request.user, current_start, current_end)
            previous_trips = self._get_trips(request.user, prev_start, prev_end)

            summary     = self._calculate_summary(current_trips, previous_trips)
            equivalents = self._get_equivalents(summary["co2_saved_g"] / 1000, request)
            cards       = self._build_cards(summary)

            recent_trips, pagination_meta = self._paginate_trips(current_trips, page, page_size)

            return Response(
                {
                    "status":      "success",
                    "timestamp":   timezone.now(),
                    "period": {
                        "type":       period_type,
                        "start_date": str(current_start),
                        "end_date":   str(current_end),
                    },
                    "summary":            summary,
                    "equivalents":        equivalents,
                    "cards":              cards,
                    "recent_trips":       recent_trips,
                    "recent_trips_meta":  pagination_meta,
                    "units": {
                        "co2":      "grams + lbs",
                        "distance": "km + miles",
                    },
                    "last_updated": timezone.now().isoformat(),
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"CO2TrackingView error: {e}", exc_info=True)
            return Response(
                {
                    "status": "error",
                    "error":  "Failed to fetch CO2 tracking data",
                    "msg":    str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # ----------------------------------------------------------
    # Date helpers
    # ----------------------------------------------------------

    def _get_date_range(self, period_type, start_date, end_date):
        today = timezone.now().date()

        if period_type == "today":
            return today, today
        elif period_type == "yesterday":
            y = today - timedelta(days=1)
            return y, y
        elif period_type == "this_week":
            return today - timedelta(days=today.weekday()), today
        elif period_type == "last_week":
            start = today - timedelta(days=today.weekday() + 7)
            return start, start + timedelta(days=6)
        elif period_type == "this_month":
            return today.replace(day=1), today
        elif period_type == "all_time":
            return today - timedelta(days=3650), today
        elif period_type == "custom" and start_date and end_date:
            return (
                datetime.strptime(start_date, "%Y-%m-%d").date(),
                datetime.strptime(end_date, "%Y-%m-%d").date(),
            )

        return today - timedelta(days=today.weekday()), today

    def _get_previous_period(self, period_type, current_start, current_end):
        delta    = (current_end - current_start) + timedelta(days=1)
        prev_end = current_start - timedelta(days=1)
        return prev_end - delta + timedelta(days=1), prev_end

    # ----------------------------------------------------------
    # DB query
    # ----------------------------------------------------------

    def _get_trips(self, user, start_date, end_date):
        return Trip.objects.filter(
            user=user,
            is_ended=True,
            is_cycle=False,
            is_archieved=False,
            start_time__date__gte=start_date,
            start_time__date__lte=end_date,
        ).order_by("-start_time")

    # ----------------------------------------------------------
    # Summary
    # ----------------------------------------------------------

    def _calculate_summary(self, current_trips, previous_trips):
        current_saved    = 0.0
        current_emitted  = 0.0

        for trip in current_trips:
            if trip.co2_saved is not None:
                if trip.co2_saved > 0:
                    current_saved   += trip.co2_saved
                else:
                    current_emitted += abs(trip.co2_saved)
            elif trip.co2_emission is not None:
                current_emitted += trip.co2_emission

        prev_saved   = 0.0
        prev_emitted = 0.0

        for trip in previous_trips:
            if trip.co2_saved is not None:
                if trip.co2_saved > 0:
                    prev_saved   += trip.co2_saved
                else:
                    prev_emitted += abs(trip.co2_saved)
            elif trip.co2_emission is not None:
                prev_emitted += trip.co2_emission

        saved_g    = round(current_saved)
        emitted_g  = round(current_emitted)
        saved_kg   = round(current_saved / 1000, 2)
        emitted_kg = round(current_emitted / 1000, 2)

        return {
            # grams
            "co2_saved_g":   saved_g,
            "co2_emitted_g": emitted_g,
            # kg
            "co2_saved_kg":   saved_kg,
            "co2_emitted_kg": emitted_kg,
            # lbs (USA/Canada)
            "co2_saved_lbs":   _g_to_lbs(saved_g),
            "co2_emitted_lbs": _g_to_lbs(emitted_g),
            # change
            "saved_change_percent":   self._calc_percent_change(prev_saved,   current_saved),
            "emitted_change_percent": self._calc_percent_change(prev_emitted, current_emitted),
            "message": self._get_message(saved_g, emitted_g),
        }

    def _calc_percent_change(self, previous, current):
        if previous == 0:
            return None if current == 0 else 100
        return round(((current - previous) / previous) * 100)

    def _get_message(self, saved_g, emitted_g):
        net = saved_g - emitted_g
        if net > 5000:
            return "Amazing! You're driving super efficiently! 🌟"
        elif net > 2000:
            return "Great job! You're making a positive impact. 🌱"
        elif net > 0:
            return "Keep up the great work!"
        elif net > -2000:
            return "Room for improvement. Try smoother acceleration."
        return "Consider eco-driving tips to reduce emissions."

    # ----------------------------------------------------------
    # Equivalents
    # ----------------------------------------------------------

    def _get_equivalents(self, saved_kg, request):
        equivalents = CO2Equivalent.objects.filter(is_active=True).order_by("priority")
        result = []
        for eq in equivalents:
            if eq.co2_kg_equivalent and eq.co2_kg_equivalent > 0 and saved_kg > 0:
                count = round(saved_kg / eq.co2_kg_equivalent, 1)
                if count >= 0.1:
                    result.append({
                        "id":         eq.id,
                        "icon_image": request.build_absolute_uri(eq.icon_image.url) if eq.icon_image else None,
                        "message":    eq.message_template.format(count=count),
                    })
        return result

    # ----------------------------------------------------------
    # Cards
    # ----------------------------------------------------------

    def _build_cards(self, summary):
        return {
            "contribution": {
                "label":          "Your Contribution",
                "type":           "avoided",
                "value_g":        summary["co2_saved_g"],
                "value_kg":       summary["co2_saved_kg"],
                "value_lbs":      summary["co2_saved_lbs"],
                "change_percent": summary["saved_change_percent"],
            },
            "still_emitted": {
                "label":          "Still Emitted",
                "type":           "released",
                "value_g":        summary["co2_emitted_g"],
                "value_kg":       summary["co2_emitted_kg"],
                "value_lbs":      summary["co2_emitted_lbs"],
                "change_percent": summary["emitted_change_percent"],
            },
        }

    # ----------------------------------------------------------
    # Recent trips
    # ----------------------------------------------------------

    def _paginate_trips(self, trips, page, page_size):
        total_count   = trips.count()
        start_idx     = (page - 1) * page_size
        paginated     = trips[start_idx: start_idx + page_size]

        trip_data = []
        for trip in paginated:

            if trip.co2_saved is not None:
                co2_g = abs(round(trip.co2_saved))
                if trip.co2_saved > 0:
                    status_val = "saved"
                    msg        = f"Nice! You saved {co2_g} g CO2"
                elif trip.co2_saved == 0:
                    status_val = "neutral"
                    msg        = "No CO2 savings for this trip"
                else:
                    status_val = "emitted"
                    msg        = f"Emitted {co2_g} g CO2"
            elif trip.co2_emission is not None:
                co2_g      = round(trip.co2_emission)
                status_val = "emitted"
                msg        = f"Trip emitted {co2_g} g CO2"
            else:
                co2_g      = 0
                status_val = "unknown"
                msg        = "CO2 data not available"

            # Distance — km + miles
            dist_km    = float(trip.distance) if trip.distance else 0.0
            dist_miles = _km_to_miles(dist_km)

            if dist_km > 0:
                if dist_km < 1:
                    dist_display_metric   = f"{int(dist_km * 1000)} m"
                    dist_display_imperial = f"{round(dist_miles * 5280)} ft"
                else:
                    dist_display_metric   = f"{dist_km:.2f} km"
                    dist_display_imperial = f"{dist_miles:.2f} mi"
            else:
                dist_display_metric   = None
                dist_display_imperial = None

            # Transport mode
            transport_mode = "car"
            vehicle_name   = None
            if trip.vehicle:
                vehicle_name = f"{trip.vehicle.make} {trip.vehicle.model}"

            trip_data.append({
                "trip_id":   f"trip_{trip.id}",
                "status":    status_val,
                # CO2
                "co2_g":     co2_g,
                "co2_kg":    round(co2_g / 1000, 4),
                "co2_lbs":   _g_to_lbs(co2_g),
                "message":   msg,
                # Distance
                "distance": {
                    "km":              round(dist_km, 2),
                    "miles":           dist_miles,
                    "display_metric":  dist_display_metric,
                    "display_imperial": dist_display_imperial,
                },
                "trip_timestamp":  trip.start_time.astimezone(pytz.utc).isoformat() if trip.start_time else None,
                "transport_mode":  transport_mode,
                "vehicle_name":    vehicle_name,
            })

        return trip_data, {
            "page":      page,
            "page_size": page_size,
            "total":     total_count,
        }