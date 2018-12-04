from django.urls import path, include
from ..api import views

urlpatterns = [
    path('', views.api_root),
    path('currency/', views.CurrencyListView.as_view(), name='currency_list'),
    path('rate/', views.EuroExchangeRate.as_view(), name='rate_list')
]