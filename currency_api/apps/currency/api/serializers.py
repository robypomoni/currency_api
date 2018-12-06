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
    rate_date = serializers.DateField()
    source_currency = serializers.CharField()
    source_amount = serializers.DecimalField(max_digits=20, decimal_places=4)
    destination_currency = serializers.CharField()
    rate = serializers.DecimalField(max_digits=20, decimal_places=4)
    amount = serializers.DecimalField(max_digits=20, decimal_places=4)



