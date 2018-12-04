from rest_framework import generics

from ..models import Currency, EuroExchangeRate
from ..api import serializers


class CurrencyListView(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = serializers.CurrencyListSerializer


class EuroExchangeRate(generics.ListAPIView):
    queryset = EuroExchangeRate.objects.all()
    serializer_class = serializers.EuroExchangeRateListSerializer
