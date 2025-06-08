from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock_quantity', 
                 'category', 'category_name', 'is_active', 'created_at', 'updated_at']
    # 包含顯示時需要的所有欄位（包含唯讀欄位）
        
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock_quantity', 'category']
        # 只包含建立時需要的欄位
    
    def validate_name(self, value):
        """驗證商品名稱"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("商品名稱至少需要2個字元")
        
        if len(value) > 100:
            raise serializers.ValidationError("商品名稱不能超過100個字元")
        
        # 檢查是否已存在相同名稱的商品
        if Product.objects.filter(name=value, is_active=True).exists():
            raise serializers.ValidationError("該商品名稱已存在")
        
        return value.strip()
    
    def validate_price(self, value):
        """驗證商品價格"""
        if value <= 0:
            raise serializers.ValidationError("商品價格必須大於0")
        
        if value > 999999:
            raise serializers.ValidationError("商品價格不能超過999,999")
        
        return value
    
    def validate_stock_quantity(self, value):
        """驗證庫存數量"""
        if value < 0:
            raise serializers.ValidationError("庫存數量不能為負數")
        
        if value > 10000:
            raise serializers.ValidationError("庫存數量不能超過10,000")
        
        return value
    
    def validate_category(self, value):
        """驗證商品類別"""
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("指定的商品類別不存在")
        
        return value
    
    def validate(self, attrs):
        """物件層級驗證"""
        name = attrs.get('name', '')
        description = attrs.get('description', '')
        
        # 檢查商品名稱和描述不能完全相同
        if name.strip().lower() == description.strip().lower():
            raise serializers.ValidationError({
                'description': '商品描述不能與商品名稱完全相同'
            })
        
        # 檢查高價商品必須有詳細描述
        price = attrs.get('price', 0)
        if price > 10000 and len(description.strip()) < 20:
            raise serializers.ValidationError({
                'description': '價格超過10,000的商品需要至少20字的詳細描述'
            })
        
        return attrs
    
    def create(self, validated_data):
        """自訂建立邏輯"""
        # 可以在這裡添加額外的建立邏輯
        # 例如：自動設定預設值、記錄日誌等
        
        # 確保新建立的商品預設為啟用狀態
        validated_data['is_active'] = True
        
        product = Product.objects.create(**validated_data)
        
        # 這裡可以添加其他邏輯，如：
        # - 發送通知
        # - 記錄操作日誌
        # - 更新相關統計資料
        
        return product