from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/currency/', include(('currency.api.urls', 'api_currency'), namespace='api_currency'))

]
