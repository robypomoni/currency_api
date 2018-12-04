from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from ..models import Currency, EuroExchangeRate
from ..api import serializers


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'currency': reverse('api_currency:currency_list', request=request, format=format),
        'rate': reverse('api_currency:rate_list', request=request, format=format)
    })


class CurrencyListView(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = serializers.CurrencyListSerializer


class EuroExchangeRate(generics.ListAPIView):
    queryset = EuroExchangeRate.objects.all()
    serializer_class = serializers.EuroExchangeRateListSerializer



