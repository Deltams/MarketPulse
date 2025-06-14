from django.http import JsonResponse
from django.db import connections


def health_check(request):
    connections["default"].ensure_connection()
    return JsonResponse({"status": "ok"})

    