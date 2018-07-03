from django.db import models

class Currency(models.Model):
    """
    Represents a currency and its exchange rate against EUR.
    """

    def __str__(self):
        return "{0.name}: {0.rate}".format(self)

    class Meta:
        verbose_name_plural = 'currencies'

    name = models.CharField(max_length=3)
    rate = models.FloatField()
