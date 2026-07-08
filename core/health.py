import logging

from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET


logger = logging.getLogger(__name__)


@require_GET
def healthz(request):
    return JsonResponse({"status": "ok"})


@require_GET
def readyz(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:
        logger.warning("Readiness database check failed.")
        return JsonResponse(
            {
                "status": "not_ready",
                "database": "error",
            },
            status=503,
        )

    return JsonResponse(
        {
            "status": "ready",
            "database": "ok",
        }
    )
