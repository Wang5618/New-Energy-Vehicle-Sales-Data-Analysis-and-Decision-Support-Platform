from django.shortcuts import render


def index(request):
    """首页/数据看板"""
    return render(request, 'dashboard/index.html')


def sales_analysis(request):
    """销售分析页面"""
    return render(request, 'dashboard/sales_analysis.html')


def brand_analysis_view(request):
    """品牌分析页面"""
    return render(request, 'dashboard/brand_analysis.html')


def region_analysis_view(request):
    """区域分析页面"""
    return render(request, 'dashboard/region_analysis.html')


def customer_analysis_view(request):
    """客户分析页面"""
    return render(request, 'dashboard/customer_analysis.html')


def inventory_analysis_view(request):
    """库存分析页面"""
    return render(request, 'dashboard/inventory_analysis.html')


def forecast_view(request):
    """预测决策页面"""
    return render(request, 'dashboard/forecast.html')
