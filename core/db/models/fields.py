from django.db.models.fields import DecimalField

class AmountField(DecimalField):
    """
    A field to represent an amount of money.
    """
    def __init__(self, verbose_name=None, name=None, max_digits=15, decimal_places=2, **kwargs):
        return super().__init__(verbose_name, name, max_digits, decimal_places, **kwargs)
