from django.contrib.auth.models import User
from rest_framework import serializers

from invoicing.models import Invoice, InvoiceLine


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class InvoiceLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLine
        fields = ["id", "label", "quantity", "unit_price"]


class InvoiceSerializer(serializers.ModelSerializer):
    lines = InvoiceLineSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = ["id", "number", "status", "description", "client", "company", "lines"]
