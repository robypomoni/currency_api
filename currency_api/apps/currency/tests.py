import decimal
import json

from django.test import TestCase
from django.urls import reverse

from .models import Currency, EuroExchangeRate

from rest_framework.test import APITestCase


class EuroExchangeRateModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        euro = Currency.objects.create(code='EUR', name='Euro')
        dollar = Currency.objects.create(code='USD', name='US Dollar')
        pound = Currency.objects.create(code='GBP', name='Pund Sterling')

        cls.euro_rate = EuroExchangeRate.objects.create(currency=euro, rate=1, date='2018-12-01')
        cls.dollar_rate = EuroExchangeRate.objects.create(currency=dollar, rate=1.18, date='2018-12-01')
        cls.pound_rate = EuroExchangeRate.objects.create(currency=pound, rate=0.89085, date='2018-12-01')

    def test_exchange(self):
        decimal.getcontext().prec = 4
        result_1 = self.euro_rate.exchange(self.dollar_rate, 1)
        result_2 = self.euro_rate.exchange(self.dollar_rate, 0)
        result_3 = self.dollar_rate.exchange(self.pound_rate, 1)

        self.assertEqual(result_1, 1.18)
        self.assertEqual(result_2, 0)
        self.assertEqual(result_3, 0.7549576271186441)


class CurrencyAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        Currency.objects.create(code='EUR', name='Euro')
        Currency.objects.create(code='USD', name='US Dollar')

    def test_currency_list(self):
        url = reverse('api_currency:currency_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['count'], Currency.objects.count())
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
        data = json.loads(response.content)
        self.assertEqual(data['count'], EuroExchangeRate.objects.count())
        self.assertContains(response, 'USD')
        self.assertContains(response, 'EUR')

