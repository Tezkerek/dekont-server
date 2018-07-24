from django.db.models import F, ExpressionWrapper, DecimalField

from rest_framework import viewsets, mixins, exceptions
from rest_framework.permissions import IsAuthenticated

from currencies.models import Currency

from .serializers import TransactionSerializer, ReporterTransactionSerializer
from .models import Transaction

class TransactionViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):

    lookup_field = 'pk'
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # User can access their and their reporters' transactions
        user = self.request.user

        # Filter by owner
        owner = self.request.query_params.get('user', None)
        if owner is not None:
            transactions = Transaction.objects.filter(user_id=owner)
        else:
            owners = list(user.reporters.values_list('pk', flat=True))
            owners.append(user.pk)

            transactions = Transaction.objects.filter(user_id__in=owners)

        # Annotate converted amount
        currency_name = self.request.query_params.get('currency', None)
        if currency_name is not None:
            try:
                currency = Currency.objects.get(name=currency_name)

                converted_amount_expression = F('sum__amount') / F('sum__currency__rate') * currency.rate
                transactions = transactions.annotate(converted_amount=ExpressionWrapper(converted_amount_expression, output_field=DecimalField()))
            except Currency.DoesNotExist:
                raise exceptions.ParseError(detail='Invalid currency')

        return transactions

    def get_serializer_class(self):
        # Approvers get a limited serializer class
        if self.action in ('update', 'partial_update'):
            transaction = self.get_object()
            if transaction.user_id != self.request.user.pk:
                # User doesn't own the transaction
                # Assume the user is an approver of the transaction's owner
                return ReporterTransactionSerializer

        return self.serializer_class
