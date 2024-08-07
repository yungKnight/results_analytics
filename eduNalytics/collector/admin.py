from django.contrib import admin

# Register your models here.
from . import models

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'entry_type', 'department')
    search_fields = ('name', 'entry_type')
    list_filter = ('entry_type', 'department')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'units', 'branch', 'department')
    search_fields = ('title', 'code')
    list_filter = ('branch', 'department')

class CourseResultAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'session', 'semester', 'grade', 'score')
    search_fields = ('course__title', 'student__name', 'session', 'semester')
    list_filter = ('session', 'semester', 'course', 'student')

admin.site.register(models.Department, DepartmentAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.CourseResult, CourseResultAdmin)