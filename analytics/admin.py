from django.contrib import admin
from .models import (
    Brand, Customer, Dealer, Inventory, MarketTrend, Region, SalesRecord, VehicleModel
)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'province', 'city', 'tier', 'population', 'gdp']
    list_filter = ['tier', 'province']
    search_fields = ['name', 'city']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'brand_type', 'founded_year', 'market_share']
    list_filter = ['brand_type', 'country']
    search_fields = ['name']


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'vehicle_type', 'power_type', 'price_min', 'price_max', 'range_km', 'is_active']
    list_filter = ['vehicle_type', 'power_type', 'brand', 'is_active']
    search_fields = ['name', 'brand__name']


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ['name', 'dealer_type', 'brand', 'region', 'rating', 'staff_count']
    list_filter = ['dealer_type', 'brand', 'region__province']
    search_fields = ['name', 'address']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'age_group', 'region', 'occupation', 'income_level', 'is_returning']
    list_filter = ['gender', 'age_group', 'income_level', 'is_returning']
    search_fields = ['name', 'phone']


@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'sale_date', 'vehicle', 'dealer', 'sale_price', 'quantity', 'channel', 'payment_method']
    list_filter = ['sale_date', 'channel', 'payment_method', 'vehicle__brand']
    search_fields = ['order_no', 'vehicle__name']
    date_hierarchy = 'sale_date'


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'dealer', 'stock_quantity', 'safety_stock', 'stock_status', 'last_updated']
    list_filter = ['vehicle__brand']
    search_fields = ['vehicle__name', 'dealer__name']


@admin.register(MarketTrend)
class MarketTrendAdmin(admin.ModelAdmin):
    list_display = ['date', 'brand', 'region', 'total_sales', 'total_revenue', 'market_share', 'growth_rate']
    list_filter = ['date', 'brand']
    date_hierarchy = 'date'
