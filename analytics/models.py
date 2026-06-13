from django.db import models


class Region(models.Model):
    """销售区域"""
    name = models.CharField('区域名称', max_length=50)
    province = models.CharField('省份', max_length=50)
    city = models.CharField('城市', max_length=50)
    tier = models.IntegerField('城市等级', choices=[(1, '一线'), (2, '二线'), (3, '三线'), (4, '四线'), (5, '五线')], default=2)
    population = models.IntegerField('人口数量(万)', default=500)
    gdp = models.DecimalField('GDP(亿元)', max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name = '销售区域'
        verbose_name_plural = '销售区域'

    def __str__(self):
        return f"{self.province}-{self.city}"


class Brand(models.Model):
    """汽车品牌"""
    BRAND_TYPES = [
        ('domestic', '国产'),
        ('joint', '合资'),
        ('foreign', '进口'),
    ]

    name = models.CharField('品牌名称', max_length=50)
    country = models.CharField('所属国家', max_length=50)
    brand_type = models.CharField('品牌类型', max_length=20, choices=BRAND_TYPES, default='domestic')
    founded_year = models.IntegerField('成立年份', default=2010)
    market_share = models.DecimalField('市场份额(%)', max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = '汽车品牌'
        verbose_name_plural = '汽车品牌'

    def __str__(self):
        return self.name


class VehicleModel(models.Model):
    """车型"""
    VEHICLE_TYPES = [
        ('sedan', '轿车'),
        ('suv', 'SUV'),
        ('mpv', 'MPV'),
        ('truck', '皮卡'),
    ]

    POWER_TYPES = [
        ('bev', '纯电动'),
        ('phev', '插电混动'),
        ('erev', '增程式'),
        ('fcev', '燃料电池'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='品牌')
    name = models.CharField('车型名称', max_length=100)
    vehicle_type = models.CharField('车辆类型', max_length=20, choices=VEHICLE_TYPES, default='sedan')
    power_type = models.CharField('动力类型', max_length=20, choices=POWER_TYPES, default='bev')
    price_min = models.DecimalField('最低价格(万元)', max_digits=10, decimal_places=2)
    price_max = models.DecimalField('最高价格(万元)', max_digits=10, decimal_places=2)
    range_km = models.IntegerField('续航里程(km)', default=400)
    battery_capacity = models.DecimalField('电池容量(kWh)', max_digits=6, decimal_places=2, default=60)
    launch_date = models.DateField('上市日期')
    is_active = models.BooleanField('是否在售', default=True)

    class Meta:
        verbose_name = '车型'
        verbose_name_plural = '车型'

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class Dealer(models.Model):
    """经销商"""
    DEALER_TYPES = [
        ('4s', '4S店'),
        ('experience', '体验中心'),
        ('direct', '直营店'),
        ('agency', '代理商'),
    ]

    name = models.CharField('经销商名称', max_length=100)
    dealer_type = models.CharField('经销商类型', max_length=20, choices=DEALER_TYPES, default='4s')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='所在区域')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='经营品牌', null=True, blank=True)
    address = models.CharField('地址', max_length=200)
    contact = models.CharField('联系方式', max_length=50, blank=True)
    store_size = models.IntegerField('店面面积(平方米)', default=500)
    staff_count = models.IntegerField('员工数量', default=20)
    rating = models.DecimalField('评分', max_digits=3, decimal_places=1, default=4.0)
    created_at = models.DateField('创建日期', auto_now_add=True)

    class Meta:
        verbose_name = '经销商'
        verbose_name_plural = '经销商'

    def __str__(self):
        return self.name


class Customer(models.Model):
    """客户"""
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]

    AGE_GROUPS = [
        ('18-25', '18-25岁'),
        ('26-35', '26-35岁'),
        ('36-45', '36-45岁'),
        ('46-55', '46-55岁'),
        ('55+', '55岁以上'),
    ]

    name = models.CharField('姓名', max_length=50)
    gender = models.CharField('性别', max_length=10, choices=GENDER_CHOICES, default='male')
    age_group = models.CharField('年龄段', max_length=20, choices=AGE_GROUPS, default='26-35')
    phone = models.CharField('电话', max_length=20, blank=True)
    email = models.EmailField('邮箱', blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='所在区域')
    occupation = models.CharField('职业', max_length=50, blank=True)
    income_level = models.IntegerField('收入水平', choices=[(1, '低'), (2, '中'), (3, '高')], default=2)
    is_returning = models.BooleanField('是否回头客', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '客户'
        verbose_name_plural = '客户'

    def __str__(self):
        return self.name


class SalesRecord(models.Model):
    """销售记录"""
    SALE_CHANNELS = [
        ('offline', '线下'),
        ('online', '线上'),
        ('phone', '电话'),
    ]

    PAYMENT_METHODS = [
        ('full', '全款'),
        ('loan', '贷款'),
        ('lease', '租赁'),
    ]

    order_no = models.CharField('订单编号', max_length=50, unique=True)
    sale_date = models.DateField('销售日期')
    vehicle = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, verbose_name='车型')
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, verbose_name='经销商')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='销售区域')
    sale_price = models.DecimalField('成交价格(万元)', max_digits=10, decimal_places=2)
    quantity = models.IntegerField('销售数量', default=1)
    channel = models.CharField('销售渠道', max_length=20, choices=SALE_CHANNELS, default='offline')
    payment_method = models.CharField('付款方式', max_length=20, choices=PAYMENT_METHODS, default='full')
    discount = models.DecimalField('优惠金额(万元)', max_digits=10, decimal_places=2, default=0)
    subsidy = models.DecimalField('补贴金额(万元)', max_digits=10, decimal_places=2, default=0)
    is_test_drive = models.BooleanField('是否试驾', default=False)
    satisfaction_score = models.IntegerField('满意度评分(1-10)', default=8)
    remarks = models.TextField('备注', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '销售记录'
        verbose_name_plural = '销售记录'
        ordering = ['-sale_date']

    def __str__(self):
        return self.order_no

    @property
    def total_amount(self):
        return self.sale_price * self.quantity


class Inventory(models.Model):
    """库存"""
    vehicle = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, verbose_name='车型')
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, verbose_name='经销商')
    stock_quantity = models.IntegerField('库存数量', default=0)
    safety_stock = models.IntegerField('安全库存', default=10)
    last_updated = models.DateTimeField('最后更新', auto_now=True)

    class Meta:
        verbose_name = '库存'
        verbose_name_plural = '库存'
        unique_together = ['vehicle', 'dealer']

    def __str__(self):
        return f"{self.vehicle} - {self.dealer}"

    @property
    def stock_status(self):
        if self.stock_quantity <= 0:
            return '缺货'
        elif self.stock_quantity < self.safety_stock:
            return '紧张'
        else:
            return '充足'


class MarketTrend(models.Model):
    """市场趋势"""
    date = models.DateField('日期')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name='区域', null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='品牌', null=True, blank=True)
    total_sales = models.IntegerField('总销量', default=0)
    total_revenue = models.DecimalField('总销售额(万元)', max_digits=15, decimal_places=2, default=0)
    market_share = models.DecimalField('市场份额(%)', max_digits=5, decimal_places=2, default=0)
    avg_price = models.DecimalField('平均价格(万元)', max_digits=10, decimal_places=2, default=0)
    growth_rate = models.DecimalField('增长率(%)', max_digits=6, decimal_places=2, default=0)

    class Meta:
        verbose_name = '市场趋势'
        verbose_name_plural = '市场趋势'
        unique_together = ['date', 'region', 'brand']
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - {self.brand or '全行业'}"
