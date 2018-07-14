from django.utils.translation import gettext_lazy as _

from rest_framework.fields import Field

from .models import Currency

class CurrencyField(Field):
    """
    Serializes a currency into its ISO code.
    """

    default_error_messages = {
        'invalid': _('Invalid currency.')
    }

    def to_representation(self, obj):
        return obj.name

    def to_internal_value(self, data):
        """
        Try to retrieve the currency instance with that name, and return it.
        """
        if not isinstance(data, str):
            self.fail('invalid')

        currency = Currency.objects.get(name=data)

        # Currency may not exist
        if currency is None:
            self.fail('invalid')

        return currency
