## `create()` 方法如何調用 `get_serializer_class()`

### 調用鏈解析

````python
# 1. 用戶發送 POST 請求到 /api/products/
# 2. Django 路由到 ProductListCreateView.as_view()
# 3. DRF 識別為 POST 請求，調用 create() 方法

def create(self, request, *args, **kwargs):
    # 4. create() 方法調用 self.get_serializer()
    serializer = self.get_serializer(data=request.data)
    #             ↑
    #           這裡是關鍵！
````

### `self.get_serializer()` 內部機制

````python
# DRF 內部的 get_serializer() 方法大致如下：
def get_serializer(self, *args, **kwargs):
    # 1. 首先調用 get_serializer_class() 獲取序列化器類別
    serializer_class = self.get_serializer_class()
    #                       ↑
    #                   這裡調用我們覆寫的方法
    
    # 2. 然後實例化序列化器
    kwargs.setdefault('context', self.get_serializer_context())
    return serializer_class(*args, **kwargs)
````

### 完整執行流程

````python
# POST 請求執行步驟：

# 1. 用戶請求
POST /api/products/ 
{
    "name": "iPhone 15",
    "price": 32900,
    "category": 1
}

# 2. DRF 調用 create() 方法
def create(self, request, *args, **kwargs):
    
    # 3. create() 調用 get_serializer()
    serializer = self.get_serializer(data=request.data)
    
    # 4. get_serializer() 內部調用 get_serializer_class()
    def get_serializer_class(self):
        if self.request.method == 'POST':  # 條件為 True
            return ProductCreateSerializer  # 返回這個類別
        return ProductSerializer
    
    # 5. 得到 ProductCreateSerializer 類別，實例化
    serializer = ProductCreateSerializer(data=request.data)
    
    # 6. 驗證和儲存
    if serializer.is_valid():
        product = serializer.save()
        
        # 7. 回傳時使用 ProductSerializer 顯示完整資訊
        return Response({
            'data': ProductSerializer(product).data
        })
````

## 為什麼要這樣設計？

### 1. **序列化器職責分離**

````python
# ProductCreateSerializer - 專注於資料驗證和建立
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock_quantity', 'category']
        # 只包含建立時需要的欄位

# ProductSerializer - 專注於資料展示
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock_quantity', 
                 'category', 'category_name', 'is_active', 'created_at', 'updated_at']
        # 包含顯示時需要的所有欄位（包含唯讀欄位）
````

### 2. **動態序列化器選擇**

````python
def get_serializer_class(self):
    # 根據不同條件返回不同序列化器
    if self.request.method == 'POST':
        return ProductCreateSerializer  # 建立時的驗證邏輯
    return ProductSerializer           # 列表時的顯示邏輯
````

## 核心概念總結

- **DRF**: Django REST Framework，API 開發框架
- **調用鏈**: `create()` → `get_serializer()` → `get_serializer_class()`
- **動態選擇**: 根據 HTTP 方法選擇合適的序列化器
- **職責分離**: 不同序列化器處理不同的業務需求

這種設計讓同一個 API 端點能夠：
- POST 時使用驗證專用的序列化器
- GET 時使用顯示專用的序列化器
- 保持程式碼的靈活性和可維護性