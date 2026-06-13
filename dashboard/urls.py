from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sales/', views.sales_analysis, name='sales_analysis'),
    path('brand/', views.brand_analysis_view, name='brand_analysis'),
    path('region/', views.region_analysis_view, name='region_analysis'),
    path('customer/', views.customer_analysis_view, name='customer_analysis'),
    path('inventory/', views.inventory_analysis_view, name='inventory_analysis'),
    path('forecast/', views.forecast_view, name='forecast'),
]
