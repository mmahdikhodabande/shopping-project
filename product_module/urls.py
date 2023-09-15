from django.urls import path
from . import views

urlpatterns = [
    # path('', views.product_list, name='product-list'),
    path('', views.ProductListView.as_view(), name='product-list'),
    path('category/<cat>', views.ProductListView.as_view(), name='category_product'),
    path('brand/<brand>', views.ProductListView.as_view(), name='brand_product'),
    # path('<slug:slug>', views.product_detail, name='product-detail'),
    path('product-favorite', views.AddProductFavorite.as_view(), name='product-favorite'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('serializer_p/', views.serializer_product.as_view(), name='product-serializer'),
    path('serializer_p_d/<pk>/', views.serializer_product_delete.as_view(), name='product-serializer_delete'),
]
