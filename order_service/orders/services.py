import requests
from django.conf import settings
from typing import Dict, Optional

class ProductService:
    """商品服務客戶端"""
    
    @staticmethod
    def get_product_info(product_id: int) -> Optional[Dict]:
        """獲取商品資訊"""
        try:
            url = f"{settings.PRODUCT_SERVICE_URL}/api/products/{product_id}/stock/"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return None
    
    @staticmethod
    def check_stock_availability(product_id: int, quantity: int) -> bool:
        """檢查庫存是否足夠"""
        product_info = ProductService.get_product_info(product_id)
        if product_info and product_info.get('success'):
            data = product_info.get('data', {})
            return data.get('stock_quantity', 0) >= quantity
        return False