from django.urls import path
from Admin_App.views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('products/', product_list, name='product_list'),
    path('products/add/', add_product, name='add_product'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', delete_product, name='delete_product'),
    path('all_order', all_order, name='all_order'),
    path('order_update/<int:order_id>/', order_update, name='order_update'),
    path('order_view/<int:order_id>/', order_view, name='order_view'),
    path('customers/', customers, name='customers'),
    path('enquiry', enquiry, name='enquiry')
]