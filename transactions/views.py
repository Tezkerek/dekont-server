from django.db.models import F, ExpressionWrapper, DecimalField

from rest_framework import viewsets, mixins, exceptions
from rest_framework.permissions import IsAuthenticated

import currencies.utils
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

    def perform_create(self, serializer):
        amount = serializer.validated_data['sum']['amount']
        print(type(amount))
        transaction = serializer.save()

        # Update the user's balance
        if amount != 0:
            transaction.user.balance_amount -= currencies.utils.convert_amount(amount, transaction.sum.currency, transaction.user.reporting_currency)
            transaction.user.save()

    def perform_update(self, serializer):
        transaction = serializer.save()

        # Update the user's balance
        # Convert the old and new amounts to the user's reporting currency
        old_currency = serializer.instance.sum.currency
        old_amount = currencies.utils.convert_amount(serializer.instance.sum.amount, old_currency, transaction.user.reporting_currency)

        sum_dict = serializer.validated_data.get('sum', {})
        new_currency = sum_dict.get('currency', old_currency)
        new_amount = currencies.utils.convert_amount(sum_dict.get('amount', old_amount), new_currency, transaction.user.reporting_currency)

        difference = new_amount - old_amount
        if difference != 0:
            transaction.user.balance_amount -= difference
            transaction.user.save()

    def perform_destroy(self, instance):
        # Update the user's balance
        instance.user.balance_amount += currencies.utils.convert_amount(instance.sum.amount, instance.sum.currency, instance.user.reporting_currency)
        instance.user.save()
        instance.delete()

    def get_queryset(self):
        # User can access their and their reporters' transactions
        user = self.request.user

        # Filter by owners
        reporting_user_ids = list(user.reporters.values_list('pk', flat=True))
        owners = self.request.query_params.getlist('users[]', None)

        if owners is None:
            # Return all transactions by default
            owners = reporting_user_ids + [user.pk]
        else:
            # Only owners that report to the current user are allowed
            invalid_owners = set(owners) - set(reporting_user_ids)
            if invalid_owners:
                raise exceptions.NotFound(detail="Users not found: " + ", ".join(invalid_owners))

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
