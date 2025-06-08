from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer
from .services import ProductService
from shared_models.serializers import BaseResponseSerializer
import uuid

class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return BaseResponseSerializer.success(data=serializer.data, message="訂單列表查詢成功")
    
    def create(self, request, *args, **kwargs):
        """建立新訂單"""
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            error_message = self._extract_error_message(serializer.errors)
            return BaseResponseSerializer.fail(
                message=error_message,
                error_code="VALIDATION_ERROR",
                data=None
            )
        
        validated_data = serializer.validated_data
        
        try:
            with transaction.atomic():
                # 計算總金額
                total_amount = sum(item['subtotal'] for item in validated_data['items'])
                
                # 建立訂單
                order = Order.objects.create(
                    order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
                    customer_name=validated_data['customer_name'],
                    customer_email=validated_data['customer_email'],
                    customer_phone=validated_data['customer_phone'],
                    shipping_address=validated_data['shipping_address'],
                    notes=validated_data.get('notes', ''),
                    total_amount=total_amount
                )
                
                # 建立訂單項目
                for item_data in validated_data['items']:
                    OrderItem.objects.create(order=order, **item_data)
                
                return BaseResponseSerializer.created(
                    data=OrderSerializer(order).data,
                    message="訂單建立成功"
                )
                
        except Exception as e:
            return BaseResponseSerializer.fail(
                message=f'訂單建立失敗: {str(e)}',
                error_code="ORDER_CREATION_FAILED",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _extract_error_message(self, errors):
        """提取第一個錯誤訊息"""
        if isinstance(errors, dict):
            for field, messages in errors.items():
                if isinstance(messages, list) and messages:
                    if field == 'non_field_errors':
                        return messages[0]
                    return messages[0]
                elif isinstance(messages, str):
                    return messages
        elif isinstance(errors, list) and errors:
            return errors[0]
        return "資料驗證失敗"

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def retrieve(self, request, *args, **kwargs):
        try:
            order = self.get_object()
            return BaseResponseSerializer.success(
                data=self.get_serializer(order).data,
                message="訂單查詢成功"
            )
        except Order.DoesNotExist:
            return BaseResponseSerializer.not_found(message="訂單不存在")

@api_view(['PATCH'])
def update_order_status(request, pk):
    """更新訂單狀態"""
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return BaseResponseSerializer.not_found(message="訂單不存在")
    
    new_status = request.data.get('status')
    if new_status not in dict(Order.STATUS_CHOICES):
        return BaseResponseSerializer.fail(
            message="無效的訂單狀態",
            error_code="INVALID_STATUS"
        )
    
    order.status = new_status
    order.save()
    
    return BaseResponseSerializer.success(
        data=OrderSerializer(order).data,
        message="訂單狀態更新成功"
    )