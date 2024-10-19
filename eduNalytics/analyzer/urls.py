from django.urls import path
from . import views

app_name = 'analyzer'

urlpatterns = [
    path('results/', views.student_cleaned_results, name='cleaned_results'),
    path('results/insight', views.display_insights, name='results_insight'),
]