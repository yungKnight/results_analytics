from django.db import models
from collector.models import Student
from django.core.validators import MaxValueValidator

class DetailedCourseResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='analyzer_results')
    level = models.CharField(max_length=20)
    semester = models.CharField(max_length=10)
    course = models.CharField(max_length=10)
    unit = models.PositiveIntegerField()
    branch = models.CharField(max_length=100)
    grade = models.CharField(
        max_length=2,
        choices=[(chr(i), chr(i)) for i in range(ord('A'), ord('F')+1)]
    )
    score = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ('student', 'level', 'semester', 'course')
        verbose_name = "Detailed Course Result"
        verbose_name_plural = "Detailed Course Results"
        ordering = ['student', 'level', 'semester', 'branch']