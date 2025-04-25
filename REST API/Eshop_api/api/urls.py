from django.contrib import admin
from django.urls import path
from api.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # Authentication and User Endpoints
    path('getUsers/', getUsers, name='getUsers'),
    path('registerUser/', registerUser, name='registerUser'),
    path('loginUser/', obtain_auth_token, name="loginUser"),
    path('logout', logoutUser, name='logoutUser'),
    path('getUserProfile', getUserProfile, name='getUserProfile'),
    path('updateUserProfile', updateUserProfile, name='updateUserProfile'),

    # Category Endpoints
    path('getCategories', getCategories, name='getCategories'),
    path('getCategory/<int:id>/', getCategory, name='getCategory'),
    path('addCategory', addCategory, name='addCategory'),
    path('updateCategory/<int:id>/', updateCategory, name='updateCategory'),
    path('deleteCategory/<int:id>/', deleteCategory, name='deleteCategory'),

    # Product Endpoints
    path('getProducts', getProducts, name='getProducts'),
    path('getProduct/<int:id>/', getProduct, name='getProduct'),
    path('getProductsByCategory/<int:c_id>/', getProductsByCategory, name='getProductsByCategory'),
    path('addProduct', addProduct, name='addProduct'),
    path('updateProduct/<int:id>/', updateProduct, name='updateProduct'),
    path('deleteProduct/<int:id>/', deleteProduct, name='deleteProduct'),

    # Cart Endpoints
    path('getCart', getCart, name='getCart'),
    path('getCartItems', getCartItems, name='getCartItems'),
    path('addToCart/<int:product_id>/<int:quantity>/', addToCart, name='addToCart'),
    path('updateCartItem/<int:cart_item_id>/<int:quantity>/', updateCartItem, name='updateCartItem'),
    path('removeCartItem/<int:cart_item_id>/', removeCartItem, name='removeCartItem'),
    path('clearCart', clearCart, name='clearCart'),

    # Order Endpoints
    path('getOrders', getOrders, name='getOrders'),                 # for admin
    path('getOrder/<int:id>/', getOrder, name='getOrder'),          # for admin
    path('createOrder', createOrder, name='createOrder'),
    path('getOrdersByUser', getOrdersByUser, name='getOrdersByUser'),
    # path('updateOrderStatus/<int:id>/', updateOrderStatus, name='updateOrderStatus'),
    # path('cancelOrder/<int:id>/', cancelOrder, name='cancelOrder'),

    # Search and Filter Endpoints
    # path('searchProducts', searchProducts, name='searchProducts'),
    # path('filterProducts', filterProducts, name='filterProducts'),

    # Checkout and Payment Endpoints
    # path('checkout', checkout, name='checkout'),
    # path('payment', payment, name='payment'),
    # path('paymentStatus', paymentStatus, name='paymentStatus'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)