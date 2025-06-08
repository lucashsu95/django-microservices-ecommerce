from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/stock/', views.product_stock_check, name='product-stock'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
]