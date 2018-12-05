from rest_framework import serializers

from ..models import Currency, EuroExchangeRate


class CurrencyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('code', 'name')


class EuroExchangeRateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EuroExchangeRate
        fields = ('rate', 'date', 'currency')


class ConvertSerializer (serializers.Serializer):
    amount = serializers.DecimalField(max_digits=20, decimal_places=4)
