from rest_framework import serializers
from .models import (
    Brand, Customer, Dealer, Inventory, MarketTrend, Region, SalesRecord, VehicleModel
)


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class VehicleModelSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    class Meta:
        model = VehicleModel
        fields = '__all__'


class DealerSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)

    class Meta:
        model = Dealer
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'


class SalesRecordSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.CharField(source='vehicle.name', read_only=True)
    brand_name = serializers.CharField(source='vehicle.brand.name', read_only=True)
    dealer_name = serializers.CharField(source='dealer.name', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    total_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = SalesRecord
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    vehicle_name = serializers.CharField(source='vehicle.name', read_only=True)
    dealer_name = serializers.CharField(source='dealer.name', read_only=True)
    stock_status = serializers.CharField(read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'


class MarketTrendSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)

    class Meta:
        model = MarketTrend
        fields = '__all__'


class SalesOverviewSerializer(serializers.Serializer):
    total_sales = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_customers = serializers.IntegerField()
    total_dealers = serializers.IntegerField()
    avg_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    month_over_month = serializers.DecimalField(max_digits=6, decimal_places=2)
    year_over_year = serializers.DecimalField(max_digits=6, decimal_places=2)


class TrendDataSerializer(serializers.Serializer):
    date = serializers.DateField()
    value = serializers.DecimalField(max_digits=15, decimal_places=2)
    label = serializers.CharField()


class BrandComparisonSerializer(serializers.Serializer):
    brand = serializers.CharField()
    sales = serializers.IntegerField()
    revenue = serializers.DecimalField(max_digits=15, decimal_places=2)
    market_share = serializers.DecimalField(max_digits=5, decimal_places=2)


class RegionSalesSerializer(serializers.Serializer):
    region = serializers.CharField()
    sales = serializers.IntegerField()
    revenue = serializers.DecimalField(max_digits=15, decimal_places=2)


class VehicleTypeDistributionSerializer(serializers.Serializer):
    type = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)


class PowerTypeDistributionSerializer(serializers.Serializer):
    type = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
