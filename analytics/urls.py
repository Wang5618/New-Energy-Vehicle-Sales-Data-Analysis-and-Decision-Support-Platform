from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'regions', views.RegionViewSet)
router.register(r'brands', views.BrandViewSet)
router.register(r'vehicles', views.VehicleModelViewSet)
router.register(r'dealers', views.DealerViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'sales', views.SalesRecordViewSet)
router.register(r'inventory', views.InventoryViewSet)
router.register(r'trends', views.MarketTrendViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('overview/', views.sales_overview, name='sales_overview'),
    path('trend/', views.sales_trend, name='sales_trend'),
    path('brand-analysis/', views.brand_analysis, name='brand_analysis'),
    path('region-analysis/', views.region_analysis, name='region_analysis'),
    path('city-analysis/', views.city_analysis, name='city_analysis'),
    path('vehicle-type/', views.vehicle_type_analysis, name='vehicle_type_analysis'),
    path('power-type/', views.power_type_analysis, name='power_type_analysis'),
    path('customer-analysis/', views.customer_analysis, name='customer_analysis'),
    path('price-range/', views.price_range_analysis, name='price_range_analysis'),
    path('channel/', views.channel_analysis, name='channel_analysis'),
    path('top-vehicles/', views.top_vehicles, name='top_vehicles'),
    path('inventory-analysis/', views.inventory_analysis, name='inventory_analysis'),
    path('forecast/', views.sales_forecast, name='sales_forecast'),
    path('satisfaction/', views.satisfaction_analysis, name='satisfaction_analysis'),
]
