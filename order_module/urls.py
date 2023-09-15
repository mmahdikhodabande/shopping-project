from django.urls import path
from . import views

urlpatterns = [
    path('Cart_order', views.Cart_orders, name='Cart_order'),
    path('add_to_order', views.add_product_to_order, name='Add_to_Order'),
    path('delete_order', views.delete_order_in_basket, name='delete_order'),
    path('change_order_detail', views.change_order_detail, name='change_order_detail'),
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify')

]
