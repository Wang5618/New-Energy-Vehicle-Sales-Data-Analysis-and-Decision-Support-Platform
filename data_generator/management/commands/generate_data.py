import random
from datetime import datetime, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from analytics.models import (
    Brand, Customer, Dealer, Inventory, MarketTrend, Region, SalesRecord, VehicleModel
)

fake = Faker('zh_CN')


class Command(BaseCommand):
    help = '生成新能源汽车销售模拟数据'

    def add_arguments(self, parser):
        parser.add_argument(
            '--records',
            type=int,
            default=10000,
            help='生成的销售记录数量（默认10000）'
        )

    def handle(self, *args, **options):
        self.stdout.write('开始生成模拟数据...')

        with transaction.atomic():
            self.create_regions()
            self.create_brands()
            self.create_vehicle_models()
            self.create_dealers()
            self.create_customers()
            self.create_sales_records(options['records'])
            self.create_inventory()
            self.create_market_trends()

        self.stdout.write(self.style.SUCCESS('数据生成完成！'))

    def create_regions(self):
        self.stdout.write('生成区域数据...')
        regions_data = [
            ('北京', '北京', 1, 2184, 43760),
            ('上海', '上海', 1, 2489, 44652),
            ('广东', '广州', 1, 1881, 28839),
            ('广东', '深圳', 1, 1768, 32387),
            ('浙江', '杭州', 2, 1237, 18753),
            ('江苏', '南京', 2, 949, 16907),
            ('四川', '成都', 2, 2126, 22074),
            ('湖北', '武汉', 2, 1365, 18866),
            ('陕西', '西安', 2, 1308, 11486),
            ('河南', '郑州', 2, 1282, 12934),
            ('湖南', '长沙', 2, 1042, 14331),
            ('山东', '青岛', 2, 1025, 14920),
            ('辽宁', '大连', 2, 745, 8752),
            ('福建', '厦门', 2, 528, 7802),
            ('江苏', '苏州', 2, 1275, 23605),
            ('浙江', '宁波', 2, 961, 15704),
            ('安徽', '合肥', 3, 947, 12013),
            ('河北', '石家庄', 3, 1122, 7100),
            ('山东', '济南', 3, 933, 12027),
            ('云南', '昆明', 3, 850, 7541),
            ('广西', '南宁', 3, 889, 5218),
            ('江西', '南昌', 3, 657, 7203),
            ('贵州', '贵阳', 3, 599, 4921),
            ('山西', '太原', 3, 544, 5571),
            ('黑龙江', '哈尔滨', 3, 1001, 5351),
            ('吉林', '长春', 3, 907, 6744),
            ('甘肃', '兰州', 4, 439, 3387),
            ('海南', '海口', 3, 290, 2057),
            ('内蒙古', '呼和浩特', 4, 350, 3322),
            ('新疆', '乌鲁木齐', 4, 405, 3893),
            ('宁夏', '银川', 4, 286, 2353),
            ('青海', '西宁', 5, 248, 1644),
            ('西藏', '拉萨', 5, 87, 742),
            ('重庆', '重庆', 2, 3213, 27894),
            ('天津', '天津', 2, 1387, 16311),
        ]

        Region.objects.all().delete()
        self.regions = []
        for province, city, tier, population, gdp in regions_data:
            region = Region.objects.create(
                name=f"{province}-{city}",
                province=province,
                city=city,
                tier=tier,
                population=population,
                gdp=Decimal(str(gdp))
            )
            self.regions.append(region)

    def create_brands(self):
        self.stdout.write('生成品牌数据...')
        brands_data = [
            ('比亚迪', '中国', 'domestic', 2003, 35.0),
            ('特斯拉', '美国', 'foreign', 2003, 14.5),
            ('蔚来', '中国', 'domestic', 2014, 5.2),
            ('小鹏', '中国', 'domestic', 2014, 4.8),
            ('理想', '中国', 'domestic', 2015, 5.5),
            ('广汽埃安', '中国', 'domestic', 2017, 6.0),
            ('极氪', '中国', 'domestic', 2021, 3.2),
            ('问界', '中国', 'domestic', 2021, 3.5),
            ('大众ID', '德国', 'joint', 2020, 4.0),
            ('宝马i', '德国', 'foreign', 2013, 3.8),
            ('奔驰EQ', '德国', 'foreign', 2019, 2.5),
            ('五菱', '中国', 'domestic', 1985, 8.0),
        ]

        Brand.objects.all().delete()
        self.brands = []
        for name, country, brand_type, founded, share in brands_data:
            brand = Brand.objects.create(
                name=name,
                country=country,
                brand_type=brand_type,
                founded_year=founded,
                market_share=Decimal(str(share))
            )
            self.brands.append(brand)

    def create_vehicle_models(self):
        self.stdout.write('生成车型数据...')
        VehicleModel.objects.all().delete()
        self.vehicles = []

        vehicle_data = [
            # 比亚迪
            (0, '秦PLUS DM-i', 'sedan', 'phev', 9.98, 14.58, 1245, 18.3, '2021-03-08'),
            (0, '汉EV', 'sedan', 'bev', 20.98, 29.98, 715, 85.4, '2020-07-12'),
            (0, '宋PLUS DM-i', 'suv', 'phev', 15.48, 21.88, 1200, 26.6, '2021-03-25'),
            (0, '海豚', 'sedan', 'bev', 11.68, 13.98, 420, 44.9, '2021-08-29'),
            (0, '海豹', 'sedan', 'bev', 21.28, 28.98, 700, 82.5, '2022-07-29'),
            (0, '元PLUS', 'suv', 'bev', 13.98, 16.78, 510, 60.5, '2022-02-19'),
            (0, '驱逐舰05', 'sedan', 'phev', 10.18, 15.78, 1245, 18.3, '2022-03-17'),
            (0, '唐DM-i', 'suv', 'phev', 20.98, 28.98, 1050, 45.8, '2021-04-19'),

            # 特斯拉
            (1, 'Model 3', 'sedan', 'bev', 23.19, 33.19, 675, 78.4, '2019-01-04'),
            (1, 'Model Y', 'suv', 'bev', 26.39, 36.39, 615, 78.4, '2021-01-01'),

            # 蔚来
            (2, 'ET5', 'sedan', 'bev', 29.80, 35.60, 560, 75.0, '2022-09-30'),
            (2, 'ES6', 'suv', 'bev', 33.80, 39.60, 490, 75.0, '2019-06-18'),
            (2, 'ET7', 'sedan', 'bev', 42.80, 50.60, 675, 100.0, '2022-03-28'),

            # 小鹏
            (3, 'P7', 'sedan', 'bev', 22.99, 33.99, 702, 80.9, '2020-04-27'),
            (3, 'G6', 'suv', 'bev', 20.99, 27.69, 755, 87.5, '2023-06-29'),
            (3, 'P5', 'sedan', 'bev', 15.69, 20.29, 460, 55.9, '2021-09-15'),
            (3, 'G9', 'suv', 'bev', 26.39, 35.99, 702, 98.0, '2022-09-21'),

            # 理想
            (4, 'L7', 'suv', 'erev', 31.98, 37.98, 1315, 42.8, '2023-02-08'),
            (4, 'L8', 'suv', 'erev', 33.98, 39.98, 1315, 42.8, '2022-09-30'),
            (4, 'L9', 'suv', 'erev', 42.98, 45.98, 1315, 44.5, '2022-06-21'),
            (4, 'MEGA', 'mpv', 'bev', 55.98, 55.98, 710, 102.7, '2024-03-01'),

            # 广汽埃安
            (5, 'AION S', 'sedan', 'bev', 13.98, 17.98, 510, 58.8, '2019-04-27'),
            (5, 'AION Y', 'suv', 'bev', 11.98, 15.38, 510, 61.7, '2021-04-19'),
            (5, 'AION V', 'suv', 'bev', 15.99, 23.29, 600, 80.0, '2020-06-16'),

            # 极氪
            (6, '001', 'sedan', 'bev', 30.00, 40.30, 741, 100.0, '2021-04-15'),
            (6, '007', 'sedan', 'bev', 20.99, 29.99, 688, 75.6, '2023-12-27'),
            (6, 'X', 'suv', 'bev', 18.98, 22.98, 560, 66.0, '2023-04-12'),

            # 问界
            (7, 'M5', 'suv', 'erev', 24.98, 27.98, 1242, 40.0, '2022-02-25'),
            (7, 'M7', 'suv', 'erev', 24.98, 32.98, 1220, 40.0, '2022-07-04'),
            (7, 'M9', 'suv', 'erev', 46.98, 56.98, 1210, 42.0, '2023-12-26'),

            # 大众ID
            (8, 'ID.3', 'sedan', 'bev', 14.99, 19.29, 450, 52.8, '2021-10-22'),
            (8, 'ID.4', 'suv', 'bev', 19.59, 29.29, 607, 84.8, '2021-01-19'),
            (8, 'ID.6', 'suv', 'bev', 25.99, 33.69, 601, 84.8, '2021-04-19'),

            # 宝马i
            (9, 'i3', 'sedan', 'bev', 35.39, 41.39, 526, 70.3, '2022-03-31'),
            (9, 'iX3', 'suv', 'bev', 40.50, 44.50, 540, 80.0, '2020-11-11'),
            (9, 'iX', 'suv', 'bev', 74.69, 99.69, 665, 111.5, '2021-12-02'),

            # 奔驰EQ
            (10, 'EQA', 'suv', 'bev', 32.20, 32.20, 619, 73.5, '2021-04-18'),
            (10, 'EQB', 'suv', 'bev', 35.20, 42.80, 600, 73.5, '2022-04-18'),
            (10, 'EQE', 'sedan', 'bev', 47.80, 53.43, 752, 96.1, '2022-08-24'),

            # 五菱
            (11, '宏光MINI EV', 'sedan', 'bev', 3.28, 9.99, 300, 26.5, '2020-07-24'),
            (11, '缤果', 'sedan', 'bev', 5.98, 8.88, 410, 37.9, '2023-03-29'),
            (11, '星光', 'sedan', 'phev', 8.88, 10.58, 1100, 20.5, '2023-12-06'),
            (11, '云朵', 'sedan', 'bev', 9.58, 13.38, 460, 50.6, '2023-08-10'),
        ]

        for brand_idx, name, vtype, ptype, price_min, price_max, range_km, battery, launch in vehicle_data:
            vehicle = VehicleModel.objects.create(
                brand=self.brands[brand_idx],
                name=name,
                vehicle_type=vtype,
                power_type=ptype,
                price_min=Decimal(str(price_min)),
                price_max=Decimal(str(price_max)),
                range_km=range_km,
                battery_capacity=Decimal(str(battery)),
                launch_date=datetime.strptime(launch, '%Y-%m-%d').date(),
                is_active=True
            )
            self.vehicles.append(vehicle)

    def create_dealers(self):
        self.stdout.write('生成经销商数据...')
        Dealer.objects.all().delete()
        self.dealers = []

        dealer_types = ['4s', 'experience', 'direct', 'agency']
        for i in range(120):
            region = random.choice(self.regions)
            brand = random.choice(self.brands)
            dealer_type = random.choice(dealer_types)
            size = random.randint(200, 2000)

            name_prefix = brand.name
            if dealer_type == '4s':
                name = f"{name_prefix}{region.city}{random.randint(1, 5)}号4S店"
            elif dealer_type == 'experience':
                name = f"{name_prefix}{region.city}体验中心"
            elif dealer_type == 'direct':
                name = f"{name_prefix}{region.city}直营店"
            else:
                name = f"{name_prefix}{region.city}代理商{random.randint(1, 10)}"

            dealer = Dealer.objects.create(
                name=name,
                dealer_type=dealer_type,
                region=region,
                brand=brand,
                address=fake.address(),
                contact=fake.phone_number(),
                store_size=size,
                staff_count=random.randint(10, 80),
                rating=Decimal(str(round(random.uniform(3.5, 5.0), 1)))
            )
            self.dealers.append(dealer)

    def create_customers(self):
        self.stdout.write('生成客户数据...')
        Customer.objects.all().delete()
        self.customers = []

        age_groups = ['18-25', '26-35', '36-45', '46-55', '55+']
        occupations = ['企业职员', '公务员', '教师', '医生', '工程师', '销售', '自由职业', '个体户', '学生', '退休人员']

        for i in range(5000):
            gender = random.choice(['male', 'female'])
            age_group = random.choices(age_groups, weights=[10, 35, 30, 15, 10])[0]
            region = random.choice(self.regions)

            customer = Customer.objects.create(
                name=fake.name(),
                gender=gender,
                age_group=age_group,
                phone=fake.phone_number(),
                email=fake.email(),
                region=region,
                occupation=random.choice(occupations),
                income_level=random.choices([1, 2, 3], weights=[30, 50, 20])[0],
                is_returning=random.random() < 0.15
            )
            self.customers.append(customer)

    def create_sales_records(self, count):
        self.stdout.write(f'生成{count}条销售记录...')
        SalesRecord.objects.all().delete()

        start_date = datetime(2020, 1, 1).date()
        end_date = datetime(2025, 5, 31).date()
        days_range = (end_date - start_date).days

        channels = ['offline', 'online', 'phone']
        payment_methods = ['full', 'loan', 'lease']

        records = []
        for i in range(count):
            sale_date = start_date + timedelta(days=random.randint(0, days_range))
            vehicle = random.choice(self.vehicles)
            dealer = random.choice(self.dealers)
            customer = random.choice(self.customers)
            region = dealer.region

            # 根据品牌调整销量权重
            brand_weight = {
                '比亚迪': 3.5, '特斯拉': 2.0, '五菱': 2.5,
                '广汽埃安': 1.5, '理想': 1.3, '蔚来': 1.0,
                '小鹏': 1.0, '问界': 1.2, '极氪': 0.8,
                '大众ID': 0.8, '宝马i': 0.5, '奔驰EQ': 0.4
            }
            weight = brand_weight.get(vehicle.brand.name, 1.0)

            # 年份影响销量
            year_factor = 1.0 + (sale_date.year - 2020) * 0.3

            # 月份影响（年底促销，春节低谷）
            month_factor = 1.0
            if sale_date.month in [1, 2]:
                month_factor = 0.7
            elif sale_date.month in [11, 12]:
                month_factor = 1.3
            elif sale_date.month in [6, 7, 8]:
                month_factor = 0.9

            if random.random() > min(0.7 * weight * year_factor * month_factor, 0.95):
                continue

            price = random.uniform(float(vehicle.price_min), float(vehicle.price_max))
            discount = random.uniform(0, price * 0.15)
            subsidy = random.uniform(0, 2.0) if vehicle.power_type in ['bev', 'phev'] else 0

            order_no = f"EV{sale_date.strftime('%Y%m%d')}{i:08d}{random.randint(10, 99)}"

            record = SalesRecord(
                order_no=order_no,
                sale_date=sale_date,
                vehicle=vehicle,
                dealer=dealer,
                customer=customer,
                region=region,
                sale_price=Decimal(str(round(price, 2))),
                quantity=1,
                channel=random.choices(channels, weights=[70, 20, 10])[0],
                payment_method=random.choices(payment_methods, weights=[55, 40, 5])[0],
                discount=Decimal(str(round(discount, 2))),
                subsidy=Decimal(str(round(subsidy, 2))),
                is_test_drive=random.random() < 0.4,
                satisfaction_score=random.randint(5, 10)
            )
            records.append(record)

            if len(records) >= 1000:
                SalesRecord.objects.bulk_create(records)
                records = []

        if records:
            SalesRecord.objects.bulk_create(records)

        self.stdout.write(f'实际生成{SalesRecord.objects.count()}条销售记录')

    def create_inventory(self):
        self.stdout.write('生成库存数据...')
        Inventory.objects.all().delete()

        inventories = []
        for vehicle in self.vehicles:
            for dealer in self.dealers:
                if dealer.brand == vehicle.brand:
                    stock = random.randint(0, 30)
                    safety = random.randint(5, 15)
                    inventories.append(Inventory(
                        vehicle=vehicle,
                        dealer=dealer,
                        stock_quantity=stock,
                        safety_stock=safety
                    ))

        Inventory.objects.bulk_create(inventories)

    def create_market_trends(self):
        self.stdout.write('生成市场趋势数据...')
        MarketTrend.objects.all().delete()

        start_date = datetime(2020, 1, 1).date()
        end_date = datetime(2025, 5, 31).date()

        trends = []
        current = start_date
        while current <= end_date:
            # 全行业月度数据
            base_sales = 15000 + (current.year - 2020) * 8000
            if current.month in [11, 12]:
                base_sales = int(base_sales * 1.3)
            elif current.month in [1, 2]:
                base_sales = int(base_sales * 0.7)

            trends.append(MarketTrend(
                date=current,
                region=None,
                brand=None,
                total_sales=int(base_sales * random.uniform(0.9, 1.1)),
                total_revenue=Decimal(str(round(base_sales * 18 * random.uniform(0.9, 1.1), 2))),
                market_share=Decimal('100.0'),
                avg_price=Decimal(str(round(18 * random.uniform(0.95, 1.05), 2))),
                growth_rate=Decimal(str(round(random.uniform(-5, 25), 2)))
            ))

            # 品牌月度数据
            for brand in self.brands:
                share = float(brand.market_share)
                brand_sales = int(base_sales * share / 100 * random.uniform(0.8, 1.2))
                avg = random.uniform(12, 35)

                trends.append(MarketTrend(
                    date=current,
                    region=None,
                    brand=brand,
                    total_sales=brand_sales,
                    total_revenue=Decimal(str(round(brand_sales * avg, 2))),
                    market_share=brand.market_share,
                    avg_price=Decimal(str(round(avg, 2))),
                    growth_rate=Decimal(str(round(random.uniform(-10, 40), 2)))
                ))

            # 计算下个月
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)

        MarketTrend.objects.bulk_create(trends, batch_size=500)
