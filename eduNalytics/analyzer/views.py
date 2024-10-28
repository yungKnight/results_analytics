from django.shortcuts import render, redirect
from .models import DetailedCourseResult
from .results_utils import (
    filter_results_by_semester,
    cleaned_results_by_semester,
    calculate_branch_gpa_for_each_semester,
    calculate_gpa_for_each_semester,
    calculate_cgpa,
    calculate_total_units_for_semester
)
from .advanced_utils import process_gpa_data
from collector.models import Student, Department
import plotly.graph_objs as go

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
            return redirect('home:home')

        filter_results_by_semester(student)

        gpa_data_by_semester = calculate_gpa_for_each_semester()
        calculate_cgpa(student)
        calculate_branch_gpa_for_each_semester()
        calculate_total_units_for_semester()

        sorted_keys = sorted(cleaned_results_by_semester.keys(), key=lambda x: (x.split()[0], x))

        serialized_cleaned_results_by_semester = {
            semester: [detailed_course_result_to_dict(result) for result in cleaned_results_by_semester[semester]]
            for semester in sorted_keys
        }

        request.session['cleaned_results_by_semester'] = serialized_cleaned_results_by_semester
        request.session['gpa_data_by_semester'] = gpa_data_by_semester

        return render(request, 'cleaned.html', {
            'student': student,
            'cleaned_results_by_semester': serialized_cleaned_results_by_semester.items(),
            'gpa_data_by_semester': gpa_data_by_semester,
        })

    return redirect('home:welcome')

def gpa_time_series_chart(request):
    """Generates a GPA time series chart from the session data."""
    gpa_data = request.session.get('gpa_data_by_semester')

    if not gpa_data:
        return redirect('home:home')

    semesters = list(gpa_data.keys())
    gpa_values = [gpa_data[semester].get('GPA') for semester in semesters]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=semesters, y=gpa_values, mode='lines+markers', name='GPA'))
    
    fig.update_layout(
        title="GPA Time Series",
        xaxis_title="Semester",
        yaxis_title="GPA",
        template="plotly_white"
    )

    chart_html = fig.to_html(full_html=False)

    return render(request, 'gpa_chart.html', {'chart': chart_html})

def cgpa_time_series_chart(request):
    """Generates a CGPA time series chart from the session data."""
    cgpa_data = request.session.get('gpa_data_by_semester')

    if not cgpa_data:
        return redirect('home:home')

    semesters = list(cgpa_data.keys())
    cgpa_values = [cgpa_data[semester].get('CGPA') for semester in semesters]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=semesters, y=cgpa_values, mode='lines+markers', name='CGPA'))

    fig.update_layout(
        title="CGPA Time Series",
        xaxis_title="Semester",
        yaxis_title="CGPA",
        template="plotly_white"
    )

    chart_html = fig.to_html(full_html=False)

    return render(request, 'cgpa_chart.html', {'chart': chart_html})

def display_insights(request):
    context = request.session.get('context')

    if context:
        processed_semester_data = process_gpa_data()
        return render(request, 'visual.html', {
            'processed_semester_data': processed_semester_data,
        })
    
    return redirect('home:welcome')

def plot_view(request):
    """Generates boxplot, scatterplot, and includes GPA and CGPA time series charts if session data is available."""
    if not request.session.get('context') or not request.session['context'].get('student_info'):
        return redirect('home:welcome')

    student_info = request.session['context'].get('student_info')
    student_name = student_info['Name']
    department_name = student_info['Department']

    try:
        department = Department.objects.get(name=department_name)
        student = Student.objects.get(name=student_name, department=department)
    except (Department.DoesNotExist, Student.DoesNotExist):
        return render(request, 'error_template.html', {"error_message": "Student or Department not found"})

    gpa_data = request.session.get('gpa_data_by_semester')
    semesters_gpa = list(gpa_data.keys()) if gpa_data else []
    gpa_values = [gpa_data[sem].get('GPA') for sem in semesters_gpa] if gpa_data else []

    gpa_fig = go.Figure()
    gpa_fig.add_trace(go.Scatter(x=semesters_gpa, y=gpa_values, mode='lines+markers', name='GPA'))
    gpa_fig.update_layout(
        xaxis_title="Semester",
        yaxis_title="GPA",
        template="plotly_white"
    )
    gpa_chart_html = gpa_fig.to_html(full_html=False)

    cgpa_values = [gpa_data[sem].get('CGPA') for sem in semesters_gpa] if gpa_data else []

    cgpa_fig = go.Figure()
    cgpa_fig.add_trace(go.Scatter(x=semesters_gpa, y=cgpa_values, mode='lines+markers', name='CGPA'))
    cgpa_fig.update_layout(
        xaxis_title="Semester",
        yaxis_title="CGPA",
        template="plotly_white"
    )
    cgpa_chart_html = cgpa_fig.to_html(full_html=False)

    return render(request, 'viss.html', {
        'gpa_chart_html': gpa_chart_html,
        'cgpa_chart_html': cgpa_chart_html
    })
