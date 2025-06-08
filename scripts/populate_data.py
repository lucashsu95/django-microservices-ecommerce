import requests
import time

BASE_URL_PRODUCT = "http://localhost:8001/api"
BASE_URL_ORDER = "http://localhost:8002/api"

def create_categories():
    """創建商品類別"""
    categories = [
        {"name": "Electronics", "description": "Electronic devices and gadgets"},
        {"name": "Clothing", "description": "Fashion and apparel items"},
        {"name": "Books", "description": "Educational and entertainment books"}
    ]
    
    print("Creating categories...")
    for category in categories:
        response = requests.post(f"{BASE_URL_PRODUCT}/categories/", json=category)
        if response.status_code == 201:
            print(f"✅ Created category: {category['name']}")
        else:
            print(f"❌ Failed to create category: {category['name']} - {response.text}")
        time.sleep(0.5)

def create_products():
    """創建商品"""
    products = [
        {
            "name": "iPhone 15 Pro",
            "description": "Latest Apple smartphone with titanium design",
            "price": 999.99,
            "stock_quantity": 25,
            "category": 1
        },
        {
            "name": "MacBook Air M3",
            "description": "Ultra-thin laptop with M3 chip",
            "price": 1299.99,
            "stock_quantity": 15,
            "category": 1
        },
        {
            "name": "Nike Air Max 270",
            "description": "Comfortable running shoes with air cushioning",
            "price": 149.99,
            "stock_quantity": 50,
            "category": 2
        },
        {
            "name": "Levis 501 Jeans",
            "description": "Classic straight fit denim jeans",
            "price": 79.99,
            "stock_quantity": 30,
            "category": 2
        },
        {
            "name": "Python Programming Guide",
            "description": "Complete guide to Python programming for beginners",
            "price": 39.99,
            "stock_quantity": 100,
            "category": 3
        }
    ]
    
    print("\nCreating products...")
    for product in products:
        response = requests.post(f"{BASE_URL_PRODUCT}/products/", json=product)
        if response.status_code == 201:
            print(f"✅ Created product: {product['name']}")
        else:
            print(f"❌ Failed to create product: {product['name']} - {response.text}")
        time.sleep(0.5)

def create_orders():
    """創建訂單"""
    orders = [
        {
            "customer_name": "John Smith",
            "customer_email": "john.smith@email.com",
            "customer_phone": "+1-555-0101",
            "shipping_address": "123 Main St, New York, NY 10001",
            "notes": "Please handle with care",
            "items": [{"product_id": 1, "quantity": 1}]
        },
        {
            "customer_name": "Emma Johnson",
            "customer_email": "emma.j@email.com",
            "customer_phone": "+1-555-0102",
            "shipping_address": "456 Oak Ave, Los Angeles, CA 90210",
            "notes": "Delivery between 9-5 PM",
            "items": [{"product_id": 2, "quantity": 1}, {"product_id": 5, "quantity": 2}]
        },
        {
            "customer_name": "Michael Brown",
            "customer_email": "m.brown@email.com",
            "customer_phone": "+1-555-0103",
            "shipping_address": "789 Pine Rd, Chicago, IL 60601",
            "notes": "Gift wrap requested",
            "items": [{"product_id": 3, "quantity": 2}]
        },
        {
            "customer_name": "Sarah Davis",
            "customer_email": "sarah.davis@email.com",
            "customer_phone": "+1-555-0104",
            "shipping_address": "321 Elm St, Houston, TX 77001",
            "notes": "Leave at front door if not home",
            "items": [{"product_id": 4, "quantity": 1}, {"product_id": 3, "quantity": 1}]
        },
        {
            "customer_name": "David Wilson",
            "customer_email": "d.wilson@email.com",
            "customer_phone": "+1-555-0105",
            "shipping_address": "654 Maple Dr, Miami, FL 33101",
            "notes": "Urgent delivery needed",
            "items": [{"product_id": 1, "quantity": 1}, {"product_id": 2, "quantity": 1}, {"product_id": 5, "quantity": 3}]
        }
    ]
    
    print("\nCreating orders...")
    for order in orders:
        response = requests.post(f"{BASE_URL_ORDER}/orders/", json=order)
        if response.status_code == 201:
            print(f"✅ Created order for: {order['customer_name']}")
        else:
            print(f"❌ Failed to create order for: {order['customer_name']} - {response.text}")
        time.sleep(0.5)

def check_services():
    """檢查服務是否運行"""
    try:
        response = requests.get(f"{BASE_URL_PRODUCT}/")
        print("✅ Product service is running")
    except requests.exceptions.ConnectionError:
        print("❌ Product service is not accessible")
        return False
    
    try:
        response = requests.get(f"{BASE_URL_ORDER}/")
        print("✅ Order service is running")
    except requests.exceptions.ConnectionError:
        print("❌ Order service is not accessible")
        return False
    
    return True

def main():
    print("🚀 Starting data population...")
    
    # 檢查服務狀態
    if not check_services():
        print("❌ Services are not running. Please start them first.")
        return
    
    # 創建假資料
    create_categories()
    create_products()
    create_orders()
    
    print("\n🎉 Data population completed!")
    print("\nYou can now test the APIs:")
    print(f"📱 Products: {BASE_URL_PRODUCT}/products/")
    print(f"📦 Orders: {BASE_URL_ORDER}/orders/")

if __name__ == "__main__":
    main()