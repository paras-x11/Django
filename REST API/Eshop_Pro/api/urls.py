from django.contrib import admin
from django.urls import path
from api.views import *
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("loginUser/", obtain_auth_token, name="loginUser"),
    path("registerUser/", registerUser, name="registerUser"),
    path("getUsers/", getUsers, name="getUsers"),

    path("categories/", CategoryAPI.as_view()),
    path("products/", ProductAPI.as_view()),
    path("cart/", CartAPI.as_view()),
    path("cart/items/", CartItemAPI.as_view()),
    path("orders/", OrderAPI.as_view()),
    path("order/items", OrderItemAPI.as_view()),
    path("orders/all/", OrderAdminAPI.as_view()),                   # for admin
    path("orders/all/<int:id>/", OrderAdminAPI.as_view()),          # for admin
]
