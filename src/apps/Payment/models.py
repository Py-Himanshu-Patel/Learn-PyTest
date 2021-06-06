import uuid

from django.db import models


class Currency(models.Model):
    """Currency model"""
    name = models.CharField(max_length=120, null=False,
                            blank=False, unique=True)
    code = models.CharField(max_length=3, null=False, blank=False, unique=True)
    symbol = models.CharField(max_length=5, null=False,
                              blank=False, default='$')

    def __str__(self) -> str:
        return self.code


class Transaction(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    currency = models.ForeignKey(
        Currency, null=False, blank=False, on_delete=models.PROTECT)
    payment_intent_id = models.CharField(
        max_length=100, null=True, blank=False, default=None)
    message = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.id} : {self.currency}"

    @property
    def link(self):
        """
            Link to a payment form for the transaction
        """
        return f'http://127.0.0.1:8000/payment/{str(self.id)}'
