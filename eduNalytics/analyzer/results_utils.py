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
gpa_data_by_semester = defaultdict(dict)

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


def calculate_gpa_for_each_semester():
    """Calculate GPA for each semester and structure it for frontend use."""
    global gpa_data_by_semester
    gpa_data_by_semester.clear()

    for semester_key, course_results in cleaned_results_by_semester.items():
        gpa = calculate_gpa(course_results)
        
        gpa_data_by_semester[semester_key] = gpa_data_by_semester.get(semester_key, {})
        gpa_data_by_semester[semester_key]['GPA'] = gpa  
        gpa_data_by_semester[semester_key]['Branch_GPA'] = gpa_data_by_semester[semester_key].get('Branch_GPA', None)  
        gpa_data_by_semester[semester_key]['CGPA'] = None 

    return gpa_data_by_semester


def calculate_branch_gpa_for_each_semester():
    """Calculate Branch GPA for each semester and append it to the GPA data."""
    global gpa_data_by_semester

    for semester_key, course_results in cleaned_results_by_semester.items():
        branch_gpa_dict = defaultdict(list)
    
        for result in course_results:
            branch = result.branch if result.branch else 'General' 
            branch_gpa_dict[branch].append(result)
        
        branch_gpa = {}
        for branch, branch_results in branch_gpa_dict.items():
            gpa = calculate_gpa(branch_results)
            branch_gpa[branch] = gpa

        if semester_key in gpa_data_by_semester:
            gpa_data_by_semester[semester_key]['Branch_GPA'] = branch_gpa
        else:
            gpa_data_by_semester[semester_key] = {
                'GPA': None, 
                'Branch_GPA': branch_gpa,
                'CGPA': None   
            }

    return gpa_data_by_semester
