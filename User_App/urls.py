from django.urls import path
from User_App.views import *


urlpatterns = [
    path('', home, name='home'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('add_to_cart_two/<int:product_id>/', add_to_cart_two, name='add_to_cart_two'),
    path('cart/list', cart_list, name='cart_list'),
    path('increase_quantity/<int:cart_id>/', increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:cart_id>/', decrease_quantity, name='decrease_quantity'),
    path('delete_cart/<int:cart_id>/', delete_cart, name='delete_cart'),
    path('product/<int:product_id>/view', product_view, name='product_view'),
    path('order', order, name='order'), 
    path('about', about, name='about'),
    path('blog', blog, name='blog'),
    path('search_results/', search_results, name='search_results'),
    path('search_suggestions/', search_suggestions, name='search_suggestions'),
    
    path('shop', shop, name='shop'),

    path('add_to_cart_three/<int:product_id>/', add_to_cart_three, name='add_to_cart_three'),

    path('profile', profile, name='profile'), 

    path('order_list', order_list, name='order_list'),

    path('add_review/<int:product_id>/', add_review, name='add_review'),

    
    
]