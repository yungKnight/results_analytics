from .models import DetailedCourseResult
from collector.models import Student
from collector.utils import get_semester  # Import the get_semester function
from django.core.exceptions import ObjectDoesNotExist
from collections import defaultdict

GRADE_POINTS = {
    'A': 5,
    'B': 4,
    'C': 3,
    'D': 2,
    'E': 1,
    'F': 0
}

cleaned_results_by_semester = defaultdict(list)

def filter_results_by_semester(student):
    """Filter detailed course results by level and semester and store in global scope."""
    global cleaned_results_by_semester
    cleaned_results_by_semester.clear()

    try:
        results = DetailedCourseResult.objects.filter(student=student).order_by('level', 'course')  # Order by course to determine semester correctly
        
        for result in results:
            # Determine semester using the get_semester function
            semester = get_semester(result.course)  # Use the function to determine the semester
            semester_key = f"{result.level} level {semester}"
            cleaned_results_by_semester[semester_key].append(result)
            
    except ObjectDoesNotExist:
        return []
        
def calculate_gpa(course_results):
    """Calculate GPA based on course results."""
    total_points = 0
    total_units = 0
    
    for result in course_results:
        grade = result.grade
        unit = result.unit
        grade_point = GRADE_POINTS.get(grade, 0)
        
        total_points += grade_point * unit
        total_units += unit
    
    if total_units == 0:
        return 0  # Avoid division by zero
    
    return total_points / total_units
