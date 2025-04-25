from django.contrib import admin
from django.urls import path,include
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name="index"),
    path('addStudent', views.addStudent, name="addStudent"),
    path('viewStudent', views.viewStudent, name="viewStudent"),
    path('edit', views.edit, name="edit"),
    path('updateStudent', views.updateStudent, name="updateStudent"),
    path('deleteStudent', views.deleteStudent, name="deleteStudent"),
    path('searchStudent', views.searchStudent, name="searchStudent"),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)