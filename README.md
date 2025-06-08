# Django Microservices E-commerce

這是一個基於 Django 的微服務電商系統專案，包含商品服務和訂單服務兩個獨立的微服務。

## 專案架構

### 微服務設計
- **Product Service** (商品服務) - 運行在端口 8001
- **Order Service** (訂單服務) - 運行在端口 8002
- **Shared Models** (共享模型) - 包含兩個服務共用的基礎模型

### 技術棧
- **後端框架**: Django + Django REST Framework
- **資料庫**: PostgreSQL (每個服務獨立資料庫)
- **容器化**: Docker + Docker Compose
- **API風格**: RESTful API

## 核心功能

### 商品服務 (product_service)
- 商品類別管理 (`Category`)
- 商品管理 (`Product`)
- 庫存查詢 API (`product_stock_check`)

### 訂單服務 (order_service)
- 訂單建立 (`create_order`)
- 訂單狀態管理 (`Order`)
- 跨服務商品資訊驗證 (`ProductService`)

### 共享組件 (shared-models)
- 基礎模型 (`BaseModel`)
- 統一回應格式 (`BaseResponseSerializer`)

## 微服務間通訊

訂單服務透過 HTTP API 呼叫商品服務來：
- 驗證商品存在性
- 檢查庫存可用性
- 獲取商品資訊用於訂單建立


## 部署方式

### 啟動系統
```bash
docker-compose up -d --build
```

### 創建數據庫遷移
```bash
# 為 product-service 創建遷移
docker-compose exec product-service python manage.py makemigrations products

# 為 order-service 創建遷移  
docker-compose exec order-service python manage.py makemigrations orders

# 應用遷移
docker-compose exec product-service python manage.py migrate
docker-compose exec order-service python manage.py migrate
```

### 資料填充

專案提供兩種方式建立測試資料：
1. Python 腳本: `populate_data.py`
2. Bash 命令: [fake-data.md](./docs/fake-data.md)

### API 測試範例

#### 商品服務 (Product Service) - 端口 8001

##### 1. 商品類別管理
**新增商品類別**
```bash
curl -X POST http://localhost:8001/api/categories/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electronics", 
    "description": "Various electronic equipment"
  }'
```

**查詢所有類別**
```bash
curl http://localhost:8001/api/categories/
```

##### 2. 商品管理
**新增商品**
```bash
curl -X POST http://localhost:8001/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15",
    "description": "Latest Apple mobile phone with advanced features",
    "price": 32900,
    "stock_quantity": 50,
    "category": 1
  }'
```

**查詢所有商品**
```bash
curl http://localhost:8001/api/products/
```

**查詢特定商品詳情**
```bash
curl http://localhost:8001/api/products/1/
```

**檢查商品庫存 (供其他服務使用)**
```bash
curl http://localhost:8001/api/products/1/stock/
```

**更新商品資訊**
```bash
curl -X PUT http://localhost:8001/api/products/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15 Pro",
    "description": "Premium Apple mobile phone with enhanced camera",
    "price": 39900,
    "stock_quantity": 30,
    "category": 1
  }'
```

**部分更新商品**
```bash
curl -X PATCH http://localhost:8001/api/products/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "price": 35900,
    "stock_quantity": 25
  }'
```

**刪除商品**
```bash
curl -X DELETE http://localhost:8001/api/products/1/
```

#### 訂單服務 (Order Service) - 端口 8002

##### 1. 訂單管理
**建立訂單**
```bash
curl -X POST http://localhost:8002/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Zhang San",
    "customer_email": "zhang@example.com",
    "customer_phone": "0912345678",
    "shipping_address": "No. 7, Section 5, Xinyi Road, Xinyi District, Taipei City",
    "notes": "Please pack carefully",
    "items": [
      {
        "product_id": "1",
        "quantity": "2"
      },
      {
        "product_id": "2",
        "quantity": "1"
      }
    ]
  }'
```

**查詢所有訂單**
```bash
curl http://localhost:8002/api/orders/
```

**查詢特定訂單詳情**
```bash
curl http://localhost:8002/api/orders/1/
```

**更新訂單狀態**
```bash
curl -X PATCH http://localhost:8002/api/orders/1/status/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "confirmed"
  }'
```

##### 2. 訂單狀態選項
可用的訂單狀態包括：
- `pending` - 待處理
- `confirmed` - 已確認
- `shipped` - 已出貨
- `delivered` - 已送達
- `cancelled` - 已取消

#### 錯誤處理範例

**商品驗證錯誤 - 名稱過短**
```bash
curl -X POST http://localhost:8001/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "X",
    "description": "Test product",
    "price": 100,
    "stock_quantity": 10,
    "category": 1
  }'
```

**訂單驗證錯誤 - 缺少必填欄位**
```bash
curl -X POST http://localhost:8002/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Test User",
    "items": []
  }'
```

**查詢不存在的資源**
```bash
curl http://localhost:8001/api/products/99999/
curl http://localhost:8002/api/orders/99999/
```

#### 回應格式範例

**成功回應格式**
```json
{
  "result": true,
  "errorCode": "",
  "message": "操作成功",
  "data": {
    "id": 1,
    "name": "iPhone 15",
    "price": "32900.00"
  }
}
```

**錯誤回應格式**
```json
{
  "result": false,
  "errorCode": "VALIDATION_ERROR",
  "message": "商品名稱至少需要2個字元",
  "data": null
}
```


## Q&A

- [Django REST Framework 中的特定方法](./docs/Django%20REST%20Framework%20中的特定方法.md)
- [DRF 是什麼](./docs/DRF%20是什麼.md)
- [create() 方法如何調用 get_serializer_class](./docs/create()%20方法如何調用%20get_serializer_class.md)