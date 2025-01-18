from django.contrib import admin
from home.models import *

# Register your models here.
if not admin.site.is_registered(Customer):
    admin.site.register(Customer)
if not admin.site.is_registered(Contact):
    admin.site.register(Contact)