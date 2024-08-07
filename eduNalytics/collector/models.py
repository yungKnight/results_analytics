from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Student(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('Diploma', 'Diploma'),
        ('UTME', 'UTME'),
    ]

    name = models.CharField(max_length=100)
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')

class Course(models.Model):
    COURSE_BRANCHES = [
        ('Microeconomics', 'Microeconomics'),
        ('Macroeconomics', 'Macroeconomics'),
        ('Mathematics for Economists', 'Mathematics for Economists'),
        ('Accessories', 'Accessories'),
    ]

    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    units = models.PositiveIntegerField()
    branch = models.CharField(max_length=30, choices=COURSE_BRANCHES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)

    class Meta:
        unique_together = ('code', 'department')

class CourseResult(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results', null=True, blank=True)
    session = models.CharField(max_length=20)
    semester = models.CharField(max_length=20)
    grade = models.CharField(max_length=5)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Course Result"
        verbose_name_plural = "Course Results"
        ordering = ['session', 'semester', 'course__code']
