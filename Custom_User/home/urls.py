from django.contrib import admin
from django.urls import path, include
from home.views  import *
urlpatterns = [
    path('', index, name="index"),
    path('index', index, name="index"),
    path('login_user', login_user, name="login_user"),
    path('signup_user', signup_user, name="signup_user"),
    path('logout_user', logout_user, name="logout_user"),
]