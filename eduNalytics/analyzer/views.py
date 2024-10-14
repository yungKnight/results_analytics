from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import DetailedCourseResult
from .results_utils import filter_results_by_semester, cleaned_results_by_semester, calculate_branch_gpa_for_each_semester, calculate_gpa_for_each_semester
from collector.models import Student

def detailed_course_result_to_dict(result):
    """Convert a DetailedCourseResult instance into a dictionary."""
    return {
        'course': result.course,
        'unit': result.unit,
        'branch': result.branch,
        'grade': result.grade,
        'score': result.score,
    }

def student_cleaned_results(request):
    context = request.session.get('context')

    if context:
        student_info = context.get('student_info')
        course_details = context.get('course_details')

        if not student_info or not course_details:
            return redirect('home:home')

        student_name = student_info.get('Name')
        entry_type = 'UTME' if student_info.get('EntryType', '').lower() == 'utme' else 'Diploma'
        student = Student.objects.filter(name=student_name, entry_type=entry_type).first()

        if not student:
            return redirect('home:welcome')

        filter_results_by_semester(student)

        gpa_data_by_semester = calculate_gpa_for_each_semester()

        calculate_branch_gpa_for_each_semester()

        sorted_keys = sorted(cleaned_results_by_semester.keys(), key=lambda x: (x.split()[0], x))

        serialized_cleaned_results_by_semester = {
            semester: [detailed_course_result_to_dict(result) for result in cleaned_results_by_semester[semester]]
            for semester in sorted_keys
        }

        context['cleaned_results_by_semester'] = serialized_cleaned_results_by_semester
        context['gpa_data_by_semester'] = gpa_data_by_semester 

        request.session.set_expiry(timedelta(minutes=15))

        return render(request, 'cleaned.html', {
            'student': student,
            'cleaned_results_by_semester': serialized_cleaned_results_by_semester.items(),
            'gpa_data_by_semester': gpa_data_by_semester.items(),
        })

    return redirect('home:welcome')
