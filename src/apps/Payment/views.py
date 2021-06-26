from rest_framework.viewsets import ModelViewSet

from apps.Payment.models import Currency, Transaction
from apps.Payment.serializers import (CurrencySerializer,
                                      FilledTransactionSerializer,
                                      UnfilledTransactionSerializer)


class CurrencyViewSet(ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class TransactionViewset(ModelViewSet):
    """ Transaction Viewset """

    queryset = Transaction.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UnfilledTransactionSerializer
        else:
            return FilledTransactionSerializer
