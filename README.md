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
2. Bash 命令: fake-data.md

### API 測試範例
1. 新增商品類別
```bash
curl -X POST http://localhost:8001/api/categories/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Electronics", "description": "Various electronic equipment"}'
```
1. 新增商品
```bash
curl -X POST http://localhost:8001/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15",
    "description": "Latest Apple mobile phone",
    "price": 32900,
    "stock_quantity": 50,
    "category": 1
  }'
```  
1. 查詢商品
```bash
curl http://localhost:8001/api/products/
```
1. 建立訂單
```bash
curl -X POST http://localhost:8002/api/orders/create/ \
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
      }
    ]
  }'
```  
1. 查詢訂單
```bash
curl http://localhost:8002/api/orders/
```
