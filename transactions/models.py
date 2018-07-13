from django.db import models
from django.core import exceptions

from users.models import User
from groups.models import Group

from currencies.models import Currency, Sum as CurrencySum

class Category(models.Model):
    """
    Represents a category of transactions.
    Categories are specific to a group, and are managed by the group admin.
    """
    name = models.CharField(max_length=100)

    # Category belongs to a group.
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='categories')

class Transaction(models.Model):
    """
    Represents a transaction.
    """
    date = models.DateField()
    description = models.CharField(max_length=100, blank=True)
    supplier = models.CharField(max_length=100, blank=True)
    document_type = models.CharField(max_length=100, blank=True)
    document_number = models.CharField(max_length=50, blank=True)
    document = models.FileField(null=True, blank=True)

    # Currency and amount
    sum = models.OneToOneField(CurrencySum, on_delete=models.PROTECT)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')

    # Transaction belongs to a single category.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='transactions', null=True, blank=True)

    def set_sum(self, amount=None, currency=None):
        """
        Sets the transaction's sum properties.
        """
        if amount is not None:
            self.sum.amount = amount

        if currency is not None:
            # Allow string or Currency instance
            if isinstance(currency, string):
                self.sum = Currency.objects.get(name=string)
            elif isinstance(currency, Currency):
                self.sum = currency
            else:
                raise AssertionError('currency must be a string or an instance of currencies.Currency')

        self.sum.save()
