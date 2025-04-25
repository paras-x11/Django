from django.contrib import admin
from api.models import *

# Register your models here.
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Like)