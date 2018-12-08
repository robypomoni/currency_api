import decimal

from django.test import TestCase
from django.urls import reverse

from .models import Currency, EuroExchangeRate

from rest_framework.test import APITestCase


class EuroExchangeRateModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        euro = Currency.objects.create(code='EUR', name='Euro')
        dollar = Currency.objects.create(code='USD', name='US Dollar')
        pound = Currency.objects.create(code='GBP', name='Pound Sterling')

        cls.euro_rate = EuroExchangeRate.objects.create(currency=euro, rate=1, date='2018-12-01')
        cls.dollar_rate = EuroExchangeRate.objects.create(currency=dollar, rate=1.18, date='2018-12-01')
        cls.pound_rate = EuroExchangeRate.objects.create(currency=pound, rate=0.89085, date='2018-12-01')

    def test_exchange(self):
        result_1 = self.euro_rate.exchange(self.dollar_rate, 15)
        result_2 = self.euro_rate.exchange(self.dollar_rate, 0)
        result_3 = self.dollar_rate.exchange(self.pound_rate, 23)

        calculated_1 = 15 / self.euro_rate.rate * self.dollar_rate.rate
        calculated_3 = 23 / self.dollar_rate.rate * self.pound_rate.rate

        self.assertEqual(result_1, calculated_1)
        self.assertEqual(result_2, 0)
        self.assertEqual(result_3, calculated_3)

    def test_exchange_rate(self):
        result_1 = self.dollar_rate.exchange_rate(self.euro_rate)
        result_2 = self.pound_rate.exchange_rate(self.euro_rate)

        self.assertEqual(result_1, 1.18)
        self.assertEqual(result_2, 0.89085)


class CurrencyAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Currency.objects.create(code='EUR', name='Euro')
        Currency.objects.create(code='USD', name='US Dollar')

    def test_currency_list(self):
        url = reverse('api_currency:currency_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], Currency.objects.count())
        self.assertContains(response, 'USD')
        self.assertContains(response, 'EUR')


class EuroExchangeRateAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        euro = Currency.objects.create(code='EUR', name='Euro')
        dollar = Currency.objects.create(code='USD', name='US Dollar')

        EuroExchangeRate.objects.create(currency=euro, rate=1, date='2018-12-01')
        EuroExchangeRate.objects.create(currency=dollar, rate=1.18, date='2018-12-01')
        EuroExchangeRate.objects.create(currency=dollar, rate=1.17, date='2018-12-03')

    def test_rate_list(self):
        url = reverse('api_currency:rate_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], EuroExchangeRate.objects.count())
        self.assertContains(response, 'USD')
        self.assertContains(response, 'EUR')


class ConvertAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        euro = Currency.objects.create(code='EUR', name='Euro')
        dollar = Currency.objects.create(code='USD', name='US Dollar')

        cls.euro_rate = EuroExchangeRate.objects.create(currency=euro, rate=1, date='2018-12-01')
        cls.dollar_rate = EuroExchangeRate.objects.create(currency=dollar, rate=1.18, date='2018-12-01')

    def test_convert_success(self):
        url = reverse(
            'api_currency:convert',
            kwargs={'src_currency': 'EUR',
                    'dest_currency': 'USD',
                    'reference_date': '2018-12-01',
                    'amount': 10.2589}
        )
        response = self.client.get(url)
        amount = decimal.Decimal(self.euro_rate.exchange(self.dollar_rate, 10.2589))
        amount_rounded = amount.quantize(decimal.Decimal('0.0001'), rounding=decimal.ROUND_HALF_UP)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['amount'], str(amount_rounded))

    def test_convert_fail(self):
        url = reverse(
            'api_currency:convert',
            kwargs={'src_currency': 'EUR',
                    'dest_currency': 'USD',
                    'reference_date': '2018-11-01',
                    'amount': 15}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        url = reverse(
            'api_currency:convert',
            kwargs={'src_currency': 'GBP',
                    'dest_currency': 'USD',
                    'reference_date': '2018-11-01',
                    'amount': 15}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


