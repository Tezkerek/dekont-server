from rest_framework import serializers

from core.serializers import DekontModelSerializer
from core.serializers import AmountField
from currencies.models import Currency, Sum
from currencies.fields import CurrencyField

from .models import Transaction, Category

class TransactionSerializer(DekontModelSerializer):
    amount = AmountField(source='sum.amount')
    currency = CurrencyField(source='sum.currency')
    converted_amount = AmountField(read_only=True)

    class Meta:
        model = Transaction
        fields = (
            'id',
            'user',
            'status',
            'date',
            'amount',
            'currency',
            'converted_amount',
            'category',
            'description',
            'supplier',
            'document_type',
            'document_number',
            'document'
        )
        read_only_fields = ('id', 'user', 'status')

    def create(self, validated_data):
        # Set the owner as the current user
        assert 'request' in self.context, "You must provide the request in the serializer's context"
        validated_data['user'] = self.context['request'].user

        # Set the amount and the currency on a related Sum model
        transaction_sum = Sum.objects.create(**validated_data.pop('sum'))

        transaction = Transaction.objects.create(**validated_data, sum=transaction_sum)

        return transaction

    def update(self, instance, validated_data):
        # Update the sum relation
        if 'sum' in validated_data:
            instance.set_sum(**validated_data.pop('sum'))

        return super().update(instance, validated_data)

class ReporterTransactionSerializer(TransactionSerializer):
    """
    TransactionSerializer for the transaction owner's approver.
    Only allows certain fields to be updated.
    """
    class Meta(TransactionSerializer.Meta):
        read_only_fields = (
            'id',
            'user',
            'date',
            'amount',
            'currency',
            'description',
            'supplier',
            'document_type',
            'document_number',
            'document'
        )

class CategorySerializer(DekontModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)
