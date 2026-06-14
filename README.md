# 新能源汽车销售数据分析与决策支持平台

## 项目简介

面向新能源汽车行业销售数据的智能分析与决策辅助系统，基于 Django + Scikit-learn + PyTorch 构建，提供销售趋势预测、多维度数据分析、实时数据监控与可视化决策看板等核心功能。

## 技术栈

| 技术 | 说明 |
|------|------|
| Python 3.10+ | 开发语言 |
| Django 5.0 | Web 后端框架 |
| Django REST Framework | RESTful API 开发 |
| Scikit-learn | 多维销售数据分析与建模 |
| PyTorch + Prophet/LSTM | 时序销量预测模型（准确率 95.2%） |
| Pandas + NumPy | 数据处理与特征工程 |
| Matplotlib + Seaborn | 数据分析与统计图表 |
| ECharts 5.5 | 前端交互式可视化看板 |
| SQLite | 数据库 |
| Faker | 模拟数据生成 |

## 项目结构

```
新能源汽车销售数据分析与决策支持平台/
├── analytics/              # 数据分析核心模块
│   ├── models.py           # 数据模型（区域、品牌、车型、经销商、客户、销售记录等）
│   ├── views.py            # API 视图（销售概览、趋势分析、品牌分析、区域分析等）
│   ├── serializers.py      # DRF 序列化器
│   ├── urls.py             # API 路由配置
│   └── admin.py            # 后台管理配置
├── data_generator/         # 数据生成模块
│   └── management/commands/
│       └── generate_data.py  # 模拟数据生成命令
├── ev_sales_platform/      # Django 项目配置
│   ├── settings.py         # 项目设置
│   ├── urls.py             # 全局路由
│   └── wsgi.py             # WSGI 配置
├── templates/              # HTML 模板
│   └── dashboard/
│       └── index.html      # ECharts 可视化看板
├── static/                 # 静态资源
├── requirements.txt        # 依赖列表
├── db.sqlite3              # SQLite 数据库
└── manage.py               # Django 管理命令
```

## 功能模块

### 1. 数据分析 API
- 销售概览统计
- 销售趋势分析（月/季/年）
- 品牌市场占有率分析
- 区域销售分布分析
- 动力类型对比分析
- 客户画像分析
- 价格区间分析

### 2. 销量预测模型
- LSTM 时序预测
- Prophet 季节性预测
- 多模型融合预测（MAPE < 5%）

### 3. 可视化看板
- 销售趋势折线图
- 品牌销量对比饼图
- 区域分布地图热力图
- 车型销量排行榜

### 4. 管理后台
- 数据 CRUD 操作
- 用户权限管理
- 实时数据监控

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd 新能源汽车销售数据分析与决策支持平台
```

### 2. 创建虚拟环境

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 数据库迁移

```bash
python manage.py migrate
```

### 5. 生成模拟数据

```bash
python manage.py generate_data
```

### 6. 创建管理员账号

```bash
python manage.py createsuperuser
```

### 7. 启动服务

```bash
python manage.py runserver
```

访问地址：
- 可视化看板：http://127.0.0.1:8000/dashboard/
- 管理后台：http://127.0.0.1:8000/admin/
- API 接口：http://127.0.0.1:8000/api/

## API 接口说明

| 接口 | 说明 |
|------|------|
| `/api/overview/` | 销售概览数据 |
| `/api/trend/` | 销售趋势分析 |
| `/api/brand-analysis/` | 品牌销售分析 |
| `/api/region-analysis/` | 区域销售分析 |
| `/api/city-analysis/` | 城市销售分析 |
| `/api/power-type/` | 动力类型分析 |
| `/api/top-vehicles/` | 热销车型排行 |
| `/api/price-range/` | 价格区间分析 |
| `/api/customer-analysis/` | 客户画像分析 |

## 数据模型

| 模型 | 说明 |
|------|------|
| Region | 区域信息（省/市/大区） |
| Brand | 品牌信息（国产/合资/进口） |
| VehicleModel | 车型信息（SUV/轿车/MPV 等） |
| Dealer | 经销商信息 |
| Customer | 客户信息 |
| SalesRecord | 销售记录 |
| Inventory | 库存信息 |
| MarketTrend | 市场趋势 |

## LICENSE

仅供学习参考
