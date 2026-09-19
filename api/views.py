import hashlib
import hmac
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from invoicing.models import Invoice

from .serializers import InvoiceSerializer, UserSerializer


class WidePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    pagination_class = WidePagination


@csrf_exempt
def quick_status(request):
    if request.method == "POST":
        data = json.loads(request.body or b"{}")
        invoice = Invoice.objects.filter(pk=data.get("id")).first()
        if invoice:
            invoice.status = data.get("status", invoice.status)
            invoice.save()
            return JsonResponse({"ok": True, "status": invoice.status})
    return JsonResponse({"ok": False}, status=400)


@csrf_exempt
def webhook(request):
    signature = request.headers.get("X-Signature", "")
    expected = hmac.new(
        settings.SECRET_KEY.encode(), request.body, hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return JsonResponse({"error": "signature invalide"}, status=403)
    return JsonResponse({"ok": True})


@api_view(["GET"])
def invoices_by_status(request):
    status = request.GET.get("status", "draft")
    qs = Invoice.objects.extra(where=["status = %s"], params=[status])
    return Response(InvoiceSerializer(qs, many=True).data)
