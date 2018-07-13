from rest_framework import serializers

from core.serializers import PkHyperlinkedModelSerializer
from currencies.models import Currency, Sum

from .models import Transaction

class TransactionSerializer(PkHyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        # Add the sum's amount and currency as direct fields
        amountField = Sum._meta.get_field('amount')
        currencyNameField = Currency._meta.get_field('name')

        self.fields['amount'] = serializers.DecimalField(
            amountField.max_digits,
            amountField.decimal_places,
            source='sum.amount'
        )

        self.fields['currency'] = serializers.CharField(
            max_length=currencyNameField.max_length,
            source='sum.currency.name'
        )

        super().__init__(*args, **kwargs)

    class Meta:
        model = Transaction
        fields = ('user', 'id', 'date', 'description', 'supplier', 'document_type', 'document_number', 'document')
