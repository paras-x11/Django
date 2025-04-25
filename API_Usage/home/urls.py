from home import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('mail', views.mail, name="mail"),
    path('sendEmail', views.sendEmail, name='sendEmail'),
    path('payment', views.payment, name='payment'),
    path('makePayment', views.makePayment, name='makePayment'),
]
