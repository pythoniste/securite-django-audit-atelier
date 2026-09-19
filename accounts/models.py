from django.conf import settings
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=200)
    siret = models.CharField(max_length=14, blank=True)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    ROLES = [
        ("admin", "Administrateur"),
        ("accountant", "Comptable"),
        ("member", "Membre"),
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="membership"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(max_length=20, choices=ROLES, default="member")
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user} @ {self.company}"
