from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from . import models

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'entry_type', 'department')
    search_fields = ('id', 'name', 'entry_type')
    list_filter = ('entry_type', 'department')

class CourseForm(ModelForm):
    class Meta:
        model = models.Course
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        department = cleaned_data.get('department')
        
        if code and department:
            if models.Course.objects.filter(code=code, department=department).exists():
                raise ValidationError({"code": "A course with this code already exists in the selected department."})
        
        return cleaned_data

class CourseOfferingInline(admin.TabularInline):
    model = models.CourseOffering
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code')
    search_fields = ('title', 'code')
    inlines = [CourseOfferingInline]

admin.site.register(models.Department, DepartmentAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.CourseBranch)
admin.site.register(models.CourseOffering)