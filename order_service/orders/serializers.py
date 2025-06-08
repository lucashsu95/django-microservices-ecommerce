from rest_framework import serializers
from .models import Order, OrderItem

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

class OrderCreateSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=100)
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField(max_length=20)
    shipping_address = serializers.CharField()
    notes = serializers.CharField(required=False, allow_blank=True)
    items = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
        min_length=1
    )
    
    def validate_items(self, value):
        """驗證訂單項目"""
        for item in value:
            if not all(k in item for k in ['product_id', 'quantity']):
                raise serializers.ValidationError('每個商品項目必須包含 product_id 和 quantity')
            try:
                int(item['product_id'])
                int(item['quantity'])
                if int(item['quantity']) <= 0:
                    raise serializers.ValidationError('商品數量必須大於 0')
            except ValueError:
                raise serializers.ValidationError('product_id 和 quantity 必須為數字')
        return value