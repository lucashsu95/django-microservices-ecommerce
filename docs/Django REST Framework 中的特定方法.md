# Django REST Framework 中的特定方法

這兩個方法是 Django REST Framework 中的**特定方法**，有固定的命名和用途。

## `get_serializer_class()` 方法

### 用途
- 動態決定使用哪個序列化器類別
- 根據不同條件（如 HTTP 方法、用戶權限等）返回不同的序列化器

### 命名規則
- **固定命名**: 必須叫 `get_serializer_class`
- DRF 會自動調用這個方法來獲取序列化器類別

### 你的程式碼解析
````python
def get_serializer_class(self):
    if self.request.method == 'POST':
        return ProductCreateSerializer  # 建立商品時使用
    return ProductSerializer           # 列出商品時使用
````

### 為什麼要這樣設計？
````python
# 不同操作可能需要不同的欄位
# POST (建立) - 可能需要驗證某些欄位
class ProductCreateSerializer(serializers.ModelSerializer):
    # 建立時的驗證邏輯
    pass

# GET (列表) - 可能需要顯示額外資訊
class ProductSerializer(serializers.ModelSerializer):
    # 列表顯示的欄位
    pass
````

## `create()` 方法

### 用途
- 處理 **POST 請求**的商品建立邏輯
- 覆寫預設的建立行為，自訂回應格式

### 命名規則
- **固定命名**: 必須叫 `create`
- `ListCreateAPIView` 會自動將 POST 請求路由到這個方法

### 你的程式碼解析
````python
def create(self, request, *args, **kwargs):
    # 1. 獲取序列化器並驗證資料
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        # 2. 儲存商品
        product = serializer.save()
        
        # 3. 自訂成功回應格式
        return Response({
            'success': True,
            'message': '商品新增成功',
            'data': ProductSerializer(product).data
        }, status=status.HTTP_201_CREATED)
    
    # 4. 自訂失敗回應格式
    return Response({
        'success': False,
        'message': '商品新增失敗',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
````

## HTTP 方法與類別方法對應

### `ListCreateAPIView` 的預設對應
````python
# HTTP GET → list() 方法
# HTTP POST → create() 方法
````

### 其他常見的固定方法名稱
````python
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    # HTTP GET → retrieve() 方法
    # HTTP PUT/PATCH → update() 方法  
    # HTTP DELETE → destroy() 方法
    
    def retrieve(self, request, *args, **kwargs):
        # 處理 GET 請求
        pass
    
    def update(self, request, *args, **kwargs):
        # 處理 PUT/PATCH 請求
        pass
    
    def destroy(self, request, *args, **kwargs):
        # 處理 DELETE 請求
        pass
````

## 總結

### 固定命名的方法
- `get_serializer_class()` - 動態選擇序列化器
- `create()` - 處理 POST 請求
- `retrieve()` - 處理 GET 單一物件
- `update()` - 處理 PUT/PATCH 請求
- `destroy()` - 處理 DELETE 請求
- `list()` - 處理 GET 列表請求

### 為什麼要覆寫？
- **自訂回應格式**: 統一 API 回應結構
- **添加業務邏輯**: 在標準 CRUD 操作中加入特殊處理
- **動態行為**: 根據不同條件使用不同邏輯

這些都是 DRF 的**約定俗成**的方法名稱，框架會自動調用對應的方法處理不同的 HTTP 請求。