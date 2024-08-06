from django.contrib import admin
from .models import Department, Student, Course, CourseResult

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

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseResult, CourseResultAdmin)
