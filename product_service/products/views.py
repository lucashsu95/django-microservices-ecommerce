from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Category
from .serializers import ProductSerializer, ProductCreateSerializer, CategorySerializer
from shared_models.serializers import BaseResponseSerializer

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductSerializer
    
    def list(self, request, *args, **kwargs):
        """GET 請求 - 商品列表"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return BaseResponseSerializer.success(
            data=serializer.data,
            message="商品列表查詢成功"
        )
    
    def create(self, request, *args, **kwargs):
        """POST 請求 - 建立商品"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return BaseResponseSerializer.created(
                data=ProductSerializer(product).data,
                message="商品新增成功"
            )
        
        # 處理驗證錯誤 - 提取第一個錯誤訊息
        error_message = self._extract_error_message(serializer.errors)
        return BaseResponseSerializer.fail(
            message=error_message,
            error_code="VALIDATION_ERROR",
            data=None
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

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """GET 請求 - 商品詳情"""
        product = self.get_object()
        return BaseResponseSerializer.success(
            data=self.get_serializer(product).data,
            message="商品查詢成功"
        )

@api_view(['GET'])
def product_stock_check(request, product_id):
    """檢查商品庫存 - 供其他服務使用"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        return BaseResponseSerializer.success(
            data={
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'stock_quantity': product.stock_quantity,
                'available': product.stock_quantity > 0
            },
            message="庫存查詢成功"
        )
    except Product.DoesNotExist:
        return BaseResponseSerializer.not_found(
            message="商品不存在",
            error_code="PRODUCT_NOT_FOUND"
        )

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def list(self, request, *args, **kwargs):
        """GET 請求 - 類別列表"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return BaseResponseSerializer.success(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """POST 請求 - 建立類別"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return BaseResponseSerializer.created(
                data=self.get_serializer(category).data,
                message="類別新增成功"
            )
        
        # 處理驗證錯誤 - 提取第一個錯誤訊息
        error_message = self._extract_error_message(serializer.errors)
        return BaseResponseSerializer.fail(
            message=error_message,
            error_code="VALIDATION_ERROR"
        )
    
    def _extract_error_message(self, errors):
        """提取第一個錯誤訊息"""
        if isinstance(errors, dict):
            for field, messages in errors.items():
                if isinstance(messages, list) and messages:
                    return messages[0]
                elif isinstance(messages, str):
                    return messages
        elif isinstance(errors, list) and errors:
            return errors[0]
        return "資料驗證失敗"