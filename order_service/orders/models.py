from django.db import models
from shared_models.models import BaseModel

class Order(BaseModel):
    STATUS_CHOICES = [
        ('pending', '待處理'),
        ('confirmed', '已確認'),
        ('shipped', '已出貨'),
        ('delivered', '已送達'),
        ('cancelled', '已取消'),
    ]
    
    order_number = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"訂單 {self.order_number}"

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.IntegerField()  # 商品服務的商品ID
    product_name = models.CharField(max_length=200)  # 冗余存儲，避免服務依賴
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)