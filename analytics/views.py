from datetime import datetime, timedelta
from decimal import Decimal

from django.db.models import Avg, Count, F, Q, Sum
from django.db.models.functions import ExtractMonth, ExtractYear, TruncMonth
from rest_framework import filters, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    Brand, Customer, Dealer, Inventory, MarketTrend, Region, SalesRecord, VehicleModel
)
from .serializers import (
    BrandSerializer, CustomerSerializer, DealerSerializer, InventorySerializer,
    MarketTrendSerializer, RegionSerializer, SalesRecordSerializer, VehicleModelSerializer
)


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filterset_fields = ['province', 'tier']
    search_fields = ['name', 'city']


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filterset_fields = ['brand_type', 'country']
    search_fields = ['name']


class VehicleModelViewSet(viewsets.ModelViewSet):
    queryset = VehicleModel.objects.all()
    serializer_class = VehicleModelSerializer
    filterset_fields = ['vehicle_type', 'power_type', 'brand', 'is_active']
    search_fields = ['name']


class DealerViewSet(viewsets.ModelViewSet):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    filterset_fields = ['dealer_type', 'brand', 'region']
    search_fields = ['name']


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_fields = ['gender', 'age_group', 'income_level', 'is_returning']
    search_fields = ['name']


class SalesRecordViewSet(viewsets.ModelViewSet):
    queryset = SalesRecord.objects.all()
    serializer_class = SalesRecordSerializer
    filterset_fields = ['sale_date', 'channel', 'payment_method', 'vehicle__brand', 'region']
    search_fields = ['order_no', 'vehicle__name']


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    filterset_fields = ['vehicle__brand']
    search_fields = ['vehicle__name', 'dealer__name']


class MarketTrendViewSet(viewsets.ModelViewSet):
    queryset = MarketTrend.objects.all()
    serializer_class = MarketTrendSerializer
    filterset_fields = ['date', 'brand', 'region']
    ordering_fields = ['date']


# ==================== 数据分析 API ====================

@api_view(['GET'])
def sales_overview(request):
    """销售概览"""
    today = datetime.now().date()
    this_month_start = today.replace(day=1)
    last_month_end = this_month_start - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    this_year_start = today.replace(month=1, day=1)
    last_year_start = this_year_start.replace(year=this_year_start.year - 1)
    last_year_end = this_year_start - timedelta(days=1)

    # 本月数据
    this_month_sales = SalesRecord.objects.filter(sale_date__gte=this_month_start)
    this_month_count = this_month_sales.count()
    this_month_revenue = this_month_sales.aggregate(total=Sum('sale_price'))['total'] or 0

    # 上月数据
    last_month_sales = SalesRecord.objects.filter(sale_date__gte=last_month_start, sale_date__lte=last_month_end)
    last_month_count = last_month_sales.count()
    last_month_revenue = last_month_sales.aggregate(total=Sum('sale_price'))['total'] or 0

    # 本月同比去年
    same_month_last_year = SalesRecord.objects.filter(
        sale_date__year=today.year - 1,
        sale_date__month=today.month
    )
    same_month_last_year_count = same_month_last_year.count()
    same_month_last_year_revenue = same_month_last_year.aggregate(total=Sum('sale_price'))['total'] or 0

    # 计算环比和同比
    mom_count = ((this_month_count - last_month_count) / last_month_count * 100) if last_month_count else 0
    yoy_count = ((this_month_count - same_month_last_year_count) / same_month_last_year_count * 100) if same_month_last_year_count else 0

    total_sales = SalesRecord.objects.count()
    total_revenue = SalesRecord.objects.aggregate(total=Sum('sale_price'))['total'] or 0
    avg_price = SalesRecord.objects.aggregate(avg=Avg('sale_price'))['avg'] or 0

    data = {
        'total_sales': total_sales,
        'total_revenue': round(total_revenue, 2),
        'total_customers': Customer.objects.count(),
        'total_dealers': Dealer.objects.count(),
        'avg_price': round(avg_price, 2),
        'this_month_sales': this_month_count,
        'this_month_revenue': round(this_month_revenue, 2),
        'month_over_month': round(mom_count, 2),
        'year_over_year': round(yoy_count, 2),
    }
    return Response(data)


@api_view(['GET'])
def sales_trend(request):
    """销售趋势"""
    period = request.GET.get('period', 'month')  # month, quarter, year
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    queryset = SalesRecord.objects.all()
    if start_date:
        queryset = queryset.filter(sale_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(sale_date__lte=end_date)

    if period == 'month':
        data = queryset.annotate(
            period=TruncMonth('sale_date')
        ).values('period').annotate(
            sales=Count('id'),
            revenue=Sum('sale_price')
        ).order_by('period')
    elif period == 'year':
        data = queryset.annotate(
            year=ExtractYear('sale_date')
        ).values('year').annotate(
            sales=Count('id'),
            revenue=Sum('sale_price')
        ).order_by('year')
    else:
        data = queryset.annotate(
            period=TruncMonth('sale_date')
        ).values('period').annotate(
            sales=Count('id'),
            revenue=Sum('sale_price')
        ).order_by('period')

    result = []
    for item in data:
        key = item.get('period') or item.get('year')
        result.append({
            'date': str(key)[:7] if period == 'month' else str(key),
            'sales': item['sales'],
            'revenue': round(float(item['revenue'] or 0), 2)
        })

    return Response(result)


@api_view(['GET'])
def brand_analysis(request):
    """品牌分析"""
    data = SalesRecord.objects.values(
        'vehicle__brand__name'
    ).annotate(
        sales=Count('id'),
        revenue=Sum('sale_price'),
        avg_price=Avg('sale_price')
    ).order_by('-sales')

    total_sales = sum(item['sales'] for item in data)

    result = []
    for item in data:
        result.append({
            'brand': item['vehicle__brand__name'],
            'sales': item['sales'],
            'revenue': round(float(item['revenue'] or 0), 2),
            'avg_price': round(float(item['avg_price'] or 0), 2),
            'market_share': round(item['sales'] / total_sales * 100, 2) if total_sales else 0
        })

    return Response(result)


@api_view(['GET'])
def region_analysis(request):
    """区域分析"""
    data = SalesRecord.objects.values(
        'region__province'
    ).annotate(
        sales=Count('id'),
        revenue=Sum('sale_price')
    ).order_by('-sales')

    result = []
    for item in data:
        result.append({
            'region': item['region__province'],
            'sales': item['sales'],
            'revenue': round(float(item['revenue'] or 0), 2)
        })

    return Response(result)


@api_view(['GET'])
def city_analysis(request):
    """城市分析"""
    data = SalesRecord.objects.values(
        'region__city', 'region__tier'
    ).annotate(
        sales=Count('id'),
        revenue=Sum('sale_price')
    ).order_by('-sales')[:20]

    result = []
    for item in data:
        result.append({
            'city': item['region__city'],
            'tier': item['region__tier'],
            'sales': item['sales'],
            'revenue': round(float(item['revenue'] or 0), 2)
        })

    return Response(result)


@api_view(['GET'])
def vehicle_type_analysis(request):
    """车型类型分析"""
    data = SalesRecord.objects.values(
        'vehicle__vehicle_type'
    ).annotate(
        sales=Count('id')
    ).order_by('-sales')

    total = sum(item['sales'] for item in data)
    type_names = {'sedan': '轿车', 'suv': 'SUV', 'mpv': 'MPV', 'truck': '皮卡'}

    result = []
    for item in data:
        sales = item['sales']
        result.append({
            'type': type_names.get(item['vehicle__vehicle_type'], item['vehicle__vehicle_type']),
            'sales': sales,
            'percentage': round(sales / total * 100, 2) if total else 0
        })

    return Response(result)


@api_view(['GET'])
def power_type_analysis(request):
    """动力类型分析"""
    data = SalesRecord.objects.values(
        'vehicle__power_type'
    ).annotate(
        sales=Count('id')
    ).order_by('-sales')

    total = sum(item['sales'] for item in data)
    type_names = {'bev': '纯电动', 'phev': '插电混动', 'erev': '增程式', 'fcev': '燃料电池'}

    result = []
    for item in data:
        sales = item['sales']
        result.append({
            'type': type_names.get(item['vehicle__power_type'], item['vehicle__power_type']),
            'sales': sales,
            'percentage': round(sales / total * 100, 2) if total else 0
        })

    return Response(result)


@api_view(['GET'])
def customer_analysis(request):
    """客户分析"""
    # 年龄分布
    age_data = Customer.objects.values('age_group').annotate(count=Count('id')).order_by('age_group')
    age_distribution = [{'group': item['age_group'], 'count': item['count']} for item in age_data]

    # 性别分布
    gender_data = Customer.objects.values('gender').annotate(count=Count('id'))
    gender_distribution = [{'gender': '男' if item['gender'] == 'male' else '女', 'count': item['count']} for item in gender_data]

    # 收入水平分布
    income_data = Customer.objects.values('income_level').annotate(count=Count('id')).order_by('income_level')
    income_names = {1: '低', 2: '中', 3: '高'}
    income_distribution = [{'level': income_names.get(item['income_level'], '未知'), 'count': item['count']} for item in income_data]

    # 回头客比例
    returning_count = Customer.objects.filter(is_returning=True).count()
    total_customers = Customer.objects.count()

    return Response({
        'age_distribution': age_distribution,
        'gender_distribution': gender_distribution,
        'income_distribution': income_distribution,
        'returning_rate': round(returning_count / total_customers * 100, 2) if total_customers else 0,
        'total_customers': total_customers
    })


@api_view(['GET'])
def price_range_analysis(request):
    """价格区间分析"""
    ranges = [
        (0, 10, '10万以下'),
        (10, 15, '10-15万'),
        (15, 20, '15-20万'),
        (20, 30, '20-30万'),
        (30, 50, '30-50万'),
        (50, 100, '50万以上'),
    ]

    result = []
    for min_price, max_price, label in ranges:
        if max_price == 100:
            count = SalesRecord.objects.filter(sale_price__gte=min_price).count()
        else:
            count = SalesRecord.objects.filter(sale_price__gte=min_price, sale_price__lt=max_price).count()
        result.append({'range': label, 'count': count})

    return Response(result)


@api_view(['GET'])
def channel_analysis(request):
    """渠道分析"""
    data = SalesRecord.objects.values('channel').annotate(count=Count('id'))
    channel_names = {'offline': '线下', 'online': '线上', 'phone': '电话'}

    result = []
    for item in data:
        result.append({
            'channel': channel_names.get(item['channel'], item['channel']),
            'count': item['count']
        })

    return Response(result)


@api_view(['GET'])
def top_vehicles(request):
    """热销车型排行"""
    limit = int(request.GET.get('limit', 10))
    data = SalesRecord.objects.values(
        'vehicle__name', 'vehicle__brand__name'
    ).annotate(
        sales=Count('id'),
        revenue=Sum('sale_price')
    ).order_by('-sales')[:limit]

    result = []
    for item in data:
        result.append({
            'vehicle': item['vehicle__name'],
            'brand': item['vehicle__brand__name'],
            'sales': item['sales'],
            'revenue': round(float(item['revenue'] or 0), 2)
        })

    return Response(result)


@api_view(['GET'])
def inventory_analysis(request):
    """库存分析"""
    low_stock = Inventory.objects.filter(stock_quantity__lt=F('safety_stock')).count()
    out_of_stock = Inventory.objects.filter(stock_quantity__lte=0).count()
    normal_stock = Inventory.objects.filter(stock_quantity__gte=F('safety_stock')).count()

    # 各品牌库存
    brand_inventory = Inventory.objects.values(
        'vehicle__brand__name'
    ).annotate(
        total_stock=Sum('stock_quantity')
    ).order_by('-total_stock')

    return Response({
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
        'normal_stock': normal_stock,
        'brand_inventory': [
            {'brand': item['vehicle__brand__name'], 'stock': item['total_stock'] or 0}
            for item in brand_inventory
        ]
    })


@api_view(['GET'])
def sales_forecast(request):
    """销售预测（简单线性预测）"""
    from django.db.models import Avg

    # 获取最近6个月的销售数据
    today = datetime.now().date()
    months_data = []
    for i in range(6, 0, -1):
        month = today.month - i
        year = today.year
        while month <= 0:
            month += 12
            year -= 1
        count = SalesRecord.objects.filter(sale_date__year=year, sale_date__month=month).count()
        months_data.append(count)

    # 简单线性预测
    if len(months_data) >= 2 and all(v > 0 for v in months_data):
        n = len(months_data)
        sum_x = sum(range(n))
        sum_y = sum(months_data)
        sum_xy = sum(i * v for i, v in enumerate(months_data))
        sum_x2 = sum(i * i for i in range(n))

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n

        forecast = []
        for i in range(1, 4):  # 预测未来3个月
            predicted = intercept + slope * (n - 1 + i)
            forecast.append({
                'month': f"+{i}月",
                'predicted': max(int(predicted), 0)
            })
    else:
        avg_sales = sum(months_data) / len(months_data) if months_data else 0
        forecast = [{'month': f"+{i}月", 'predicted': int(avg_sales)} for i in range(1, 4)]

    return Response({
        'historical': months_data,
        'forecast': forecast
    })


@api_view(['GET'])
def satisfaction_analysis(request):
    """满意度分析"""
    avg_score = SalesRecord.objects.aggregate(avg=Avg('satisfaction_score'))['avg'] or 0

    score_distribution = SalesRecord.objects.values('satisfaction_score').annotate(
        count=Count('id')
    ).order_by('satisfaction_score')

    # 按品牌分析满意度
    brand_satisfaction = SalesRecord.objects.values(
        'vehicle__brand__name'
    ).annotate(
        avg_score=Avg('satisfaction_score')
    ).order_by('-avg_score')[:10]

    return Response({
        'average_score': round(float(avg_score), 2),
        'score_distribution': [
            {'score': item['satisfaction_score'], 'count': item['count']}
            for item in score_distribution
        ],
        'brand_satisfaction': [
            {'brand': item['vehicle__brand__name'], 'score': round(float(item['avg_score']), 2)}
            for item in brand_satisfaction
        ]
    })
