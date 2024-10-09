from django.contrib import admin
from .models import DetailedCourseResult  

class DetailedCourseResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'level', 'semester', 'course', 'unit', 'branch', 'grade', 'score')  # Fields to display in the list view
    list_filter = ('level', 'semester', 'branch', 'grade')  # Fields to filter by in the admin panel
    search_fields = ('student__name', 'course', 'level', 'semester')  # Fields to search by in the admin panel

    readonly_fields = ('student', 'level', 'semester', 'course', 'unit', 'branch', 'grade', 'score')

    fieldsets = (
        (None, {
            'fields': readonly_fields
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

admin.site.register(DetailedCourseResult, DetailedCourseResultAdmin)
