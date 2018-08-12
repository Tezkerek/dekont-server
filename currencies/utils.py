from .models import Currency

def _get_currency(obj):
    """
    Shortcut for getting a currency from a string or a currency instance.
    """
    return obj if isinstance(obj, Currency) else Currency.objects.get(name=obj)

def convert_amount(amount, from_currency, to_currency):
    """
    Convert the amount from a currency to another.
    from_currency and to_currency may be a currency name or an instance of the Currency class.
    """

    from_currency = _get_currency(from_currency)
    to_currency = _get_currency(to_currency)

    return amount / from_currency.rate * to_currency.rate

def convert_amount_to_base(amount, from_currency):
    """
    Converts the amount from a currency to the base currency.
    """
    return amount / _get_currency(from_currency).rate
