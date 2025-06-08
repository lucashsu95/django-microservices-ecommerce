from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Category
from .serializers import ProductSerializer, ProductCreateSerializer, CategorySerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response({
                'result': True,
                'errorCode': '',
                'message': '商品新增成功',
                'data': ProductSerializer(product).data
            }, status=status.HTTP_201_CREATED)
        
        # 提取第一個錯誤訊息
        error_message = self._extract_error_message(serializer.errors)
        return Response({
            'result': False,
            'errorCode': 'VALIDATION_ERROR',
            'message': error_message,
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def _extract_error_message(self, errors):
        """提取第一個錯誤訊息"""
        if isinstance(errors, dict):
            for field, messages in errors.items():
                if isinstance(messages, list) and messages:
                    return messages[0]
        return "資料驗證失敗"

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        return Response({
            'result': True,
            'errorCode': '',
            'message': '商品查詢成功',
            'data': self.get_serializer(product).data
        })

@api_view(['GET'])
def product_stock_check(request, product_id):
    """檢查商品庫存 - 供其他服務使用"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        return Response({
            'result': True,
            'errorCode': '',
            'message': '庫存查詢成功',
            'data': {
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'stock_quantity': product.stock_quantity,
                'available': product.stock_quantity > 0
            }
        })
    except Product.DoesNotExist:
        return Response({
            'result': False,
            'errorCode': 'PRODUCT_NOT_FOUND',
            'message': '商品不存在',
            'data': None
        }, status=status.HTTP_404_NOT_FOUND)

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer