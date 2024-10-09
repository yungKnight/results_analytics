from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxValueValidator

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CourseBranch(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='branches')

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    ENTRY_TYPE_CHOICES = [
        ('Diploma', 'Diploma'),
        ('UTME', 'UTME'),
    ]

    name = models.CharField(max_length=100)
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.id} - {self.name}"

class Course(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.title} ({self.code})"

class CourseOffering(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='offerings')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='course_offerings')
    branch = models.ForeignKey(CourseBranch, on_delete=models.CASCADE, related_name='course_offerings')
    units = models.PositiveIntegerField()

    class Meta:
        unique_together = ('course', 'department')

    def __str__(self):
        return f"{self.course.code} ({self.branch.name} - {self.department.name})"

class CourseResult(models.Model):
    session = models.CharField(
        max_length=9,
        validators=[RegexValidator(regex=r'^\d{4}/\d{4}$', message='Session must be in the format YYYY/YYYY')]
    )
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, to_field='id', on_delete=models.CASCADE, related_name='results')
    grade = models.CharField(
        max_length=2,
        choices=[(chr(i), chr(i)) for i in range(ord('A'), ord('F')+1)]
    )
    score = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)]
    )
    semester = models.CharField(max_length=10, editable=False)
    level = models.CharField(max_length=20, editable=False)  

    def __str__(self):
        return f"{self.course_offering.course} - {self.student} - {self.session} {self.semester} {self.grade} {self.score}"

    class Meta:
        verbose_name = "Course Result"
        verbose_name_plural = "Course Results"
        ordering = ['session', 'course_offering__course__code']