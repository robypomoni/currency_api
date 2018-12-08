import decimal

from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from ..models import Currency, EuroExchangeRate
from ..api import serializers


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'currency': reverse('api_currency:currency_list', request=request, format=format),
        'rate': reverse('api_currency:rate_list', request=request, format=format),
        'convert': reverse('api_currency:convert_instructions', request=request, format=format)
    })


class CurrencyListView(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = serializers.CurrencyListSerializer


class EuroExchangeRateListView(generics.ListAPIView):
    queryset = EuroExchangeRate.objects.all()
    serializer_class = serializers.EuroExchangeRateListSerializer


class ConvertInstructionsView(APIView):
    """
    Usage Instructions:
    To convert currency make a GET HTTP request following this format:
    /api/currency/convert/"source_currency"/"dest_currency"/"date"/"amount/
    where currencies are expressed with ISO codes, date in in format YYYY-MM-GG
    and amount is a number with up to 4 decimal places. For example:

    /api/currency/convert/USD/EUR/2018-12-06/120.25

    """
    def get(self, request, *args, **kwargs):
        return Response('OK')


class ConvertView(APIView):

    def get(self, request, *args, **kwargs):
        date = self.kwargs['reference_date']
        src_currency = self.kwargs['src_currency']
        dest_currency = self.kwargs['dest_currency']
        amount = decimal.Decimal(self.kwargs['amount'])

        rates = EuroExchangeRate.objects.filter(date=date)

        if rates:
            try:
                dest_rate = rates.get(currency=dest_currency)
            except EuroExchangeRate.DoesNotExist:
                raise NotFound(detail='There is no currency with code {}'.format(dest_currency))
            try:
                src_rate = rates.get(currency=src_currency)
            except EuroExchangeRate.DoesNotExist:
                raise NotFound(detail='There is no currency with code {}'.format(dest_currency))
            result = src_rate.exchange(dest_rate, amount)
            rate = src_rate.exchange_rate(dest_rate)
        else:
            raise NotFound(detail='There are no rates for date {}'.format(date))

        obj = {
            'rate_date': date,
            'source_currency': src_currency,
            'source_amount': amount,
            'destination_currency': dest_currency,
            'amount': result,
            'rate': rate
        }
        serializer = serializers.ConvertSerializer(obj)
        return Response(serializer.data)
