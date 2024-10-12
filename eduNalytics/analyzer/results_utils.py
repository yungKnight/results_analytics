from .models import DetailedCourseResult
from collector.models import Student
from collector.utils import get_semester
from django.core.exceptions import ObjectDoesNotExist
from collections import defaultdict
import re

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
        results = DetailedCourseResult.objects.filter(student=student).order_by('level', 'course')

        for result in results:
            semester = get_semester(result.course)
            
            level = re.search(r'\d+', result.level).group(0) if re.search(r'\d+', result.level) else result.level
            formatted_level = f"{level} level" if 'level' not in result.level else result.level.strip()
            
            semester_key = f"{formatted_level} {semester}".strip()
            
            if semester_key not in cleaned_results_by_semester:
                cleaned_results_by_semester[semester_key] = []
            
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
        return 0 
    
    return total_points / total_units
