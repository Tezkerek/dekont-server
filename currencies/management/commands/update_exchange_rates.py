import urllib.request
import json

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from currencies.models import Currency

class Command(BaseCommand):
    help = 'Updates the currencies exchange rates.'

    def handle(self, *args, **options):
        rates = self.get_rates()

        # Update existing currencies' rates, and insert new currencies.
        for name, rate in rates.items():
            Currency.objects.update_or_create(
                name=name,
                defaults={'rate': rate}
            )

        self.stdout.write(self.style.SUCCESS('Successfully updated exchange rates.'))

    def get_rates(self):
        """
        Retrieves the exchange rates.
        """
        app_id = settings.OPEN_EXCHANGE_RATES_KEY
        url = 'https://openexchangerates.org/api/latest.json?app_id={}'.format(app_id)

        response = urllib.request.urlopen(url)
        content = json.loads(response.read())

        # Raise exception is server errors out
        if response.status != 200:
            raise CommandError(
                'Failed: {0} "{1}"'.format(
                    response.status,
                    content.get('description', "No description provided")
                )
            )


        return content['rates']

