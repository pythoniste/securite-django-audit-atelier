import uuid

from django.db import models

from invoicing.models import ExpenseNote


class ShareLink(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expense = models.ForeignKey(
        ExpenseNote, on_delete=models.CASCADE, related_name="shares"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.token)
