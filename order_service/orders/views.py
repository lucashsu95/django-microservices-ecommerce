from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer
from .services import ProductService
import uuid

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        return Response({
            'success': True,
            'message': '訂單查詢成功',
            'data': self.get_serializer(order).data
        })

@api_view(['POST'])
def create_order(request):
    """建立新訂單"""
    serializer = OrderCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': '資料驗證失敗',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    
    try:
        with transaction.atomic():
            # 1. 驗證商品並獲取資訊
            order_items_data = []
            total_amount = 0
            
            for item_data in validated_data['items']:
                product_id = int(item_data['product_id'])
                quantity = int(item_data['quantity'])
                
                # 檢查商品存在性和庫存
                product_info = ProductService.get_product_info(product_id)
                if not product_info or not product_info.get('success'):
                    return Response({
                        'success': False,
                        'message': f'商品 ID {product_id} 不存在'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                product_data = product_info['data']
                if not ProductService.check_stock_availability(product_id, quantity):
                    return Response({
                        'success': False,
                        'message': f'商品 {product_data["name"]} 庫存不足'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                unit_price = float(product_data['price'])
                subtotal = unit_price * quantity
                total_amount += subtotal
                
                order_items_data.append({
                    'product_id': product_id,
                    'product_name': product_data['name'],
                    'unit_price': unit_price,
                    'quantity': quantity,
                    'subtotal': subtotal
                })
            
            # 2. 建立訂單
            order = Order.objects.create(
                order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
                customer_name=validated_data['customer_name'],
                customer_email=validated_data['customer_email'],
                customer_phone=validated_data['customer_phone'],
                shipping_address=validated_data['shipping_address'],
                notes=validated_data.get('notes', ''),
                total_amount=total_amount
            )
            
            # 3. 建立訂單項目
            for item_data in order_items_data:
                OrderItem.objects.create(order=order, **item_data)
            
            return Response({
                'success': True,
                'message': '訂單建立成功',
                'data': OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response({
            'success': False,
            'message': f'訂單建立失敗: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PATCH'])
def update_order_status(request, pk):
    """更新訂單狀態"""
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({
            'success': False,
            'message': '訂單不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    
    new_status = request.data.get('status')
    if new_status not in dict(Order.STATUS_CHOICES):
        return Response({
            'success': False,
            'message': '無效的訂單狀態'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    order.status = new_status
    order.save()
    
    return Response({
        'success': True,
        'message': '訂單狀態更新成功',
        'data': OrderSerializer(order).data
    })