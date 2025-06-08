from rest_framework import serializers
from .models import Order, OrderItem
from .services import ProductService

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'product_name', 'unit_price', 'quantity', 'subtotal']
        read_only_fields = ['subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'customer_name', 'customer_email', 
                 'customer_phone', 'shipping_address', 'status', 'total_amount', 
                 'notes', 'items', 'created_at', 'updated_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
        min_length=1,
        write_only=True,
        error_messages={'required': '訂單項目為必填欄位', 'min_length': '至少需要一個訂單項目'}
    )
    
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_phone', 
                 'shipping_address', 'notes', 'items']
        extra_kwargs = {
            'customer_name': {'error_messages': {'required': '客戶姓名為必填欄位'}},
            'customer_email': {'error_messages': {'required': '客戶Email為必填欄位', 'invalid': 'Email格式不正確'}},
            'customer_phone': {'error_messages': {'required': '客戶電話為必填欄位'}},
            'shipping_address': {'error_messages': {'required': '送貨地址為必填欄位'}},
        }
    
    def validate_items(self, value):
        """驗證訂單項目"""
        validated_items = []
        
        for i, item in enumerate(value):
            # 檢查必要欄位
            if not all(k in item for k in ['product_id', 'quantity']):
                raise serializers.ValidationError(f'第{i+1}個商品項目必須包含 product_id 和 quantity')
            
            try:
                product_id = int(item['product_id'])
                quantity = int(item['quantity'])
                
                if quantity <= 0:
                    raise serializers.ValidationError(f'第{i+1}個商品的數量必須大於 0')
                
                # 檢查商品是否存在
                product_info = ProductService.get_product_info(product_id)
                if not product_info or not product_info.get('result'):
                    raise serializers.ValidationError(f'商品 ID {product_id} 不存在')
                
                product_data = product_info['data']
                
                # 檢查庫存
                if not ProductService.check_stock_availability(product_id, quantity):
                    raise serializers.ValidationError(f'商品 {product_data["name"]} 庫存不足')
                
                # 計算價格
                unit_price = float(product_data['price'])
                subtotal = unit_price * quantity
                
                validated_items.append({
                    'product_id': product_id,
                    'product_name': product_data['name'],
                    'unit_price': unit_price,
                    'quantity': quantity,
                    'subtotal': subtotal
                })
                
            except ValueError:
                raise serializers.ValidationError(f'第{i+1}個商品的 product_id 和 quantity 必須為數字')
            except Exception as e:
                raise serializers.ValidationError(f'第{i+1}個商品驗證失敗: {str(e)}')
        
        return validated_items