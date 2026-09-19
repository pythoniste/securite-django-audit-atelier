from django.conf import settings
from django.db import models

from accounts.models import Company


class Client(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="clients")
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="projects")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="projects")
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    STATUS = [("draft", "Brouillon"), ("sent", "Envoyée"), ("paid", "Payée")]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="invoices")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="invoices")
    number = models.CharField(max_length=30)
    status = models.CharField(max_length=10, choices=STATUS, default="draft")
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="lines")
    label = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class ExpenseNote(models.Model):
    STATUS = [
        ("draft", "Brouillon"),
        ("submitted", "Soumise"),
        ("approved", "Approuvée"),
        ("reimbursed", "Remboursée"),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="expenses")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expenses"
    )
    label = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=12, choices=STATUS, default="draft")
    receipt = models.FileField(upload_to="receipts/", blank=True, null=True)
    reimbursed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.label} ({self.amount})"
