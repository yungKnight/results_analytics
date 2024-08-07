from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxValueValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('Diploma', 'Diploma'),
        ('UTME', 'UTME'),
    ]

    name = models.CharField(max_length=100)
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.name

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

    def __str__(self):
        return f"{self.title} ({self.code})"

class CourseResult(models.Model):
    SEMESTER_CHOICES = [
        ('Harmattan', 'Harmattan'),
        ('Rain', 'Rain'),
    ]

    session = models.CharField(
        max_length=9,
        validators=[RegexValidator(regex=r'^\d{4}/\d{4}$', message='Session must be in the format YYYY/YYYY')]
    )
    semester = models.CharField(max_length=9, choices=SEMESTER_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results', null=True, blank=True)
    grade = models.CharField(
        max_length=2,
        choices=[(chr(i), chr(i)) for i in range(ord('A'), ord('F')+1)]
    )
    score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MaxValueValidator(100)]
    )

    def clean(self):
        if self.score > 100:
            raise ValidationError('Score must be less than or equal to 100.')

    def save(self, *args, **kwargs):
        if self.session and len(self.session) == 8 and self.session[4] != '/':
            self.session = f"{self.session[:4]}/{self.session[4:]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course} - {self.student} - {self.session} {self.semester} {self.grade} {self.score}"

    class Meta:
        verbose_name = "Course Result"
        verbose_name_plural = "Course Results"
        ordering = ['session', 'semester', 'course__code']
