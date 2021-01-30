from django.urls import path

from . import views

urlpatterns = [
    path('topStocks', views.topStocks, name='topStocks'),
    path('searchStock', views.searchStock, name='searchStock'),
]