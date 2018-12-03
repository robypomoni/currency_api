from django.contrib import admin
from .models import Currency, EuroExchangeRate


class EuroExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'rate', 'date')


admin.site.register(Currency)
admin.site.register(EuroExchangeRate, EuroExchangeRateAdmin)
