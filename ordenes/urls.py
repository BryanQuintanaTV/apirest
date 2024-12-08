from django.urls import path
from .views import OrderList, OrderDetail

urlpatterns = [
    path('api/v1/ordenes/', OrderList.as_view(), name='order-list'),
    path('api/v1/ordenes/<int:id>/', OrderDetail.as_view(), name='order-detail'),
]