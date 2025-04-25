from django.contrib import admin
from studentApp.models import *

# Register your models here.

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['deptName']


class StudentIdAdmin(admin.ModelAdmin):
    list_display = ['student_id']
      
class StudentAdmin(admin.ModelAdmin):
    list_display = ['firstName', 'lastName']

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subjectName']

class MarkAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject']

admin.site.register(Department,DepartmentAdmin)
admin.site.register(StudentId,StudentIdAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Mark,MarkAdmin)