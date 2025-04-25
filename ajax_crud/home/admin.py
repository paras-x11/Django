from django.contrib import admin
from home.models import *

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "phone"]

admin.site.register(Student, StudentAdmin)