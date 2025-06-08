from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/status/', views.update_order_status, name='order-status-update'),
]