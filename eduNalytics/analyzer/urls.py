from django.urls import path
from . import views

app_name = 'analyzer'

urlpatterns = [
    path('your-cleaned-results/', views.student_cleaned_results, name='cleaned_results'),
]