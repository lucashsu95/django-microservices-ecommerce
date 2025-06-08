from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseModel(models.Model):
    """共用基礎模型"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class ProductReference(BaseModel):
    """商品參考模型 - 在訂單服務中使用"""
    id = models.BigAutoField(primary_key=True)
    product_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'product_reference'