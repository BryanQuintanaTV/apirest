from django.urls import path
from .views import ProductList, ProductDetail

urlpatterns = [
    path('api/v1/productos/', ProductList.as_view(), name='product-list'),
    path('api/v1/productos/<int:id>/', ProductDetail.as_view(), name='product-detail'),
]