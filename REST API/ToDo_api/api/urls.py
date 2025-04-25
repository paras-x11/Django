from django.contrib import admin
from django.urls import path
from api.views import *
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),        # login to get token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("getUser/" , getUser, name="getUser"),
    path("registerUser/" , registerUser, name="registerUser"),
    path("todo/", TodoAPI.as_view(), name="todo"),
    path("todo/<int:task_id>/" , TodoAPI.as_view(), name="todoById"),


]
