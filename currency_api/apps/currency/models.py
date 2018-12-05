from django.db import models
from model_utils.models import StatusModel, TimeStampedModel
from model_utils import Choices


class Currency (models.Model):
    """
    Model to store currency
    """
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return '{} - {}'.format(self.code, self.name)


class EuroExchangeRate(StatusModel, TimeStampedModel):
    """
    Model to store Euro exchange rates by date
    """
    STATUS = Choices('active', 'disabled')
    currency = models.ForeignKey(Currency, related_name="exchange_rates", on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=20, decimal_places=4)
    date = models.DateField()

    class Meta:
        verbose_name_plural = "Euro Exchange Rates"
        verbose_name = "Euro Exchange Rate"
        get_latest_by = 'date'

    def __str__(self):
        return '{} - {}'.format(self.currency.code, self.date)
