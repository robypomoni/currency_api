import requests

from django.core.management.base import BaseCommand

from ...models import Currency


class Command(BaseCommand):
    help = 'Download currencies list from https://openexchangerates.org'

    def handle(self, *args, **options):
        response = requests.get('https://openexchangerates.org/api/currencies.json')
        data = response.json()
        for key, value in data.items():
            currency = Currency(code=key, name=value)
            currency.save()
            message = 'created {}'.format(key)
            print(message)
