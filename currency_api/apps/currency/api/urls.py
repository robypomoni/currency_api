from django.urls import path, re_path
from ..api import views

urlpatterns = [
    path('', views.api_root),
    path('currency/', views.CurrencyListView.as_view(), name='currency_list'),
    path('rate/', views.EuroExchangeRateListView.as_view(), name='rate_list'),
    re_path(
        'convert/(?P<src_currency>[A-Z]{3})/(?P<dest_currency>[A-Z]{3})/'
        '(?P<reference_date>\d{4}-\d{2}-\d{2})/(?P<amount>\d+\.{0,1}\d{0,4})$',
        views.Convert.as_view(),
        name='convert'
    )

]
