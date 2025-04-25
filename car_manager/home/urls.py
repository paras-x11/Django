from django.urls import path
from home.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name="index"),
    path('index/', index, name="index"),

    path('add/car/', car_form, name="car_form"),

    path('add/', add_car, name='add_car'),

    path('car/<int:id>/', car_detail, name='car_detail'),

    path('edit/car/<int:id>/', edit_car, name='edit_car'),

    path('delete/car/<int:id>/', delete_car, name='delete_car'),

    path('car/list/', car_list, name="car_list"),

    path('getCars/', getCars, name='getCars'),
    
    path('about/', about, name='about'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)