import requests
import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand

from ...models import EuroExchangeRate, Currency


class Command(BaseCommand):
    help = 'Download rates of the last 90 days from https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'

    def handle(self, *args, **options):
        response = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml')
        tree = ET.fromstring(response.text)
        for date in tree[2]:
            currency = Currency.objects.get(code='EUR')
            rate = EuroExchangeRate(
                date=date.attrib['time'],
                currency=currency,
                rate=1
            )
            rate.save()
            message = 'created {} - EUR'.format(date.attrib['time'])
            print(message)
            for item in date:
                try:
                    currency = Currency.objects.get(code=item.attrib['currency'])
                    rate = EuroExchangeRate(
                        date=date.attrib['time'],
                        currency=currency,
                        rate=item.attrib['rate']
                    )
                    rate.save()
                    message = 'created {} - {}'.format(date.attrib['time'], currency)
                    print(message)
                except Currency.DoesNotExist:
                    print('Currency {} does not exist in the database'.format(currency))
