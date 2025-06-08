這個錯誤是因為在 bash 中使用了 Windows 的命令行語法。在 bash 中需要使用不同的語法。

請使用以下修正版本：

````bash
# 1. 創建商品類別
curl -X POST http://localhost:8001/api/categories/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Electronics", "description": "Electronic devices and gadgets"}'

curl -X POST http://localhost:8001/api/categories/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Clothing", "description": "Fashion and apparel items"}'

curl -X POST http://localhost:8001/api/categories/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Books", "description": "Educational and entertainment books"}'

# 2. 創建商品
curl -X POST http://localhost:8001/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "iPhone 15 Pro", "description": "Latest Apple smartphone with titanium design", "price": 999.99, "stock_quantity": 25, "category": 1}'

curl -X POST http://localhost:8001/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "MacBook Air M3", "description": "Ultra-thin laptop with M3 chip", "price": 1299.99, "stock_quantity": 15, "category": 1}'

curl -X POST http://localhost:8001/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Nike Air Max 270", "description": "Comfortable running shoes with air cushioning", "price": 149.99, "stock_quantity": 50, "category": 2}'

curl -X POST http://localhost:8001/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Levis 501 Jeans", "description": "Classic straight fit denim jeans", "price": 79.99, "stock_quantity": 30, "category": 2}'

curl -X POST http://localhost:8001/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Python Programming Guide", "description": "Complete guide to Python programming for beginners", "price": 39.99, "stock_quantity": 100, "category": 3}'

# 3. 創建訂單
curl -X POST http://localhost:8002/api/orders/create/ \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "John Smith", "customer_email": "john.smith@email.com", "customer_phone": "+1-555-0101", "shipping_address": "123 Main St, New York, NY 10001", "notes": "Please handle with care", "items": [{"product_id": 1, "quantity": 1}]}'

curl -X POST http://localhost:8002/api/orders/create/ \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "Emma Johnson", "customer_email": "emma.j@email.com", "customer_phone": "+1-555-0102", "shipping_address": "456 Oak Ave, Los Angeles, CA 90210", "notes": "Delivery between 9-5 PM", "items": [{"product_id": 2, "quantity": 1}, {"product_id": 5, "quantity": 2}]}'

curl -X POST http://localhost:8002/api/orders/create/ \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "Michael Brown", "customer_email": "m.brown@email.com", "customer_phone": "+1-555-0103", "shipping_address": "789 Pine Rd, Chicago, IL 60601", "notes": "Gift wrap requested", "items": [{"product_id": 3, "quantity": 2}]}'

curl -X POST http://localhost:8002/api/orders/create/ \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "Sarah Davis", "customer_email": "sarah.davis@email.com", "customer_phone": "+1-555-0104", "shipping_address": "321 Elm St, Houston, TX 77001", "notes": "Leave at front door if not home", "items": [{"product_id": 4, "quantity": 1}, {"product_id": 3, "quantity": 1}]}'

curl -X POST http://localhost:8002/api/orders/create/ \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "David Wilson", "customer_email": "d.wilson@email.com", "customer_phone": "+1-555-0105", "shipping_address": "654 Maple Dr, Miami, FL 33101", "notes": "Urgent delivery needed", "items": [{"product_id": 1, "quantity": 1}, {"product_id": 2, "quantity": 1}, {"product_id": 5, "quantity": 3}]}'
````