from rest_framework import serializers

from core.serializers import PkHyperlinkedModelSerializer
from currencies.models import Currency, Sum
from currencies.fields import CurrencyField

from .models import Transaction

amountField = Sum._meta.get_field('amount')

class TransactionSerializer(PkHyperlinkedModelSerializer):
    amount = serializers.DecimalField(
        amountField.max_digits,
        amountField.decimal_places,
        source='sum.amount'
    )

    currency = CurrencyField(source='sum.currency')

    class Meta:
        model = Transaction
        fields = ('user', 'id', 'date', 'amount', 'currency', 'description', 'supplier', 'document_type', 'document_number', 'document')
        read_only_fields = ('user',)

    def create(self, validated_data):
        # Set the owner as the current user
        assert 'request' in self.context, "You must provide the request in the serializer's context"
        validated_data['user'] = self.context['request'].user

        # Set the amount and the currency on a related Sum model
        transaction_sum = Sum.objects.create(**validated_data.pop('sum'))

        transaction = Transaction.objects.create(**validated_data, sum=transaction_sum)

        return transaction
