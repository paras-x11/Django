from django.contrib import admin
from api.models import *

# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'is_completed', 'created_at', 'updated_at')
    list_filter = ('is_completed', 'user')  # Add filters for easier navigation
    search_fields = ('title', 'description')  # Enable search by title and description
    ordering = ('-created_at',)  # Show the latest todos first

admin.site.register(Todo, TodoAdmin)