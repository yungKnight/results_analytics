from django.db import models

class Course(models.Model):
    COURSE_BRANCHES = [
        ('Microeconomics', 'Microeconomics'),
        ('Macroeconomics', 'Macroeconomics'),
        ('Mathematics for Economists', 'Mathematics for Economists'),
        ('Accessories', 'Accessories'),
    ]

    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    units = models.PositiveIntegerField()
    branch = models.CharField(max_length=30, choices=COURSE_BRANCHES)


class CourseResult(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='results')
    session = models.CharField(max_length=20)
    semester = models.CharField(max_length=20)
    grade = models.CharField(max_length=5)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = "Course Result"
        verbose_name_plural = "Course Results"
        ordering = ['session', 'semester', 'course__code']
