import requests
from django.conf import settings
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

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
        except requests.RequestException as e:
            logger.error(f"請求商品 {product_id} 時發生錯誤: {str(e)}")
        except Exception as e:
            logger.error(f"獲取商品 {product_id} 資訊時發生未預期錯誤: {str(e)}")
        return None
    
    @staticmethod
    def check_stock_availability(product_id: int, quantity: int) -> bool:
        """檢查庫存是否足夠"""
        product_info = ProductService.get_product_info(product_id)
        if product_info and product_info.get('result'):
            data = product_info.get('data', {})
            return data.get('stock_quantity', 0) >= quantity
        return False