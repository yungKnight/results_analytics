import pandas as pd
import pingouin as pg
import time
import json

from django.shortcuts import render, redirect
from .models import DetailedCourseResult

from .results_utils import (
    filter_results_by_semester,
    cleaned_results_by_semester,
    calculate_branch_gpa_for_each_semester,
    calculate_gpa_for_each_semester,
    calculate_cgpa,
    calculate_total_units_for_semester)
from .advanced_utils import process_gpa_data
from collector.models import Student, Department
from .inference_utils import (
    extract_cleaned_results_df, extract_gpa_data_df,
    extract_branch_gpa_df,  calculate_branch_semester_avg_scores,
    calculate_semester_avg_scores,  calculate_correlations,
    count_courses_per_branch,   calculate_branch_units, calculate_partial_correlations,
    calculate_ema)
from .visualizer_utils import (
    extract_branch_gpa_data,    branch_colors,  extract_combined_gpa_cgpa_data,
    extract_from_cleaned_semester,    extract_passed_courses_from_cleaned_semester,
    generate_branch_gpa_chart,    generate_combined_gpa_cgpa_chart,    generate_boxplot_charts,
    generate_scatter_plot,  generate_overall_branch_representation_pie_chart,
    generate_branch_distribution_pie_charts,    generate_semester_score_charts,
    generate_grouped_bar_chart_for_courses_and_pass_rate,
    generate_branch_distribution_stacked_bar_chart,
)
from .decision_utils import (display_parsed_emas, extract_correlations, get_correlation, 
    extract_partial_corr)

def detailed_course_result_to_dict(result):
    """Convert a DetailedCourseResult instance into a dictionary."""
    return {
        'course': result.course,
        'unit': result.unit,
        'branch': result.branch,
        'grade': result.grade,
        'score': result.score,
    }

def get_student_from_context(request):
    """Helper function to retrieve student and course details from session context."""
    context = request.session.get('context')

    if context:
        student_info = context.get('student_info')
        course_details = context.get('course_details')

        if not student_info or not course_details:
            return None, None

        student_name = student_info.get('Name')
        entry_type = 'UTME' if student_info.get('EntryType', '').lower() == 'utme' else 'Diploma'
        student = Student.objects.filter(name=student_name, entry_type=entry_type).first()

        if not student:
            return None, None 

        return student, course_details 

    return None, None  

def student_cleaned_results(request):
    """Displays cleaned results for a student."""
    student, course_details = get_student_from_context(request)
    if not student:
        return redirect('home:welcome')

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

def display_insights(request):
    """Displays insights based on processed GPA data."""

    student, _ = get_student_from_context(request)
    if not student:
        return redirect('home:welcome')

    cleaned_results = request.session.get('cleaned_results_by_semester')
    gpa_data = request.session.get('gpa_data_by_semester')

    cleaned_results_df = extract_cleaned_results_df(cleaned_results)
    branch_counts_df = count_courses_per_branch(cleaned_results)
    gpa_data_df = extract_gpa_data_df(gpa_data, cleaned_results)
    branch_gpa_df = extract_branch_gpa_df(gpa_data)
    branch_total_units_df = calculate_branch_units(cleaned_results)

    branch_columns = branch_gpa_df.columns

    robust_ema_df = gpa_data_df.drop(columns=[
            'branch_gpa',
            'total_units',
            'semester_course_count'
        ])

    parameters = ['gpa', 'cgpa']
    span = 4
    
    robust_ema_df = calculate_ema(robust_ema_df, parameters, span)

    if len(branch_columns) > 1:
        robust_ema_df = robust_ema_df.merge(
            branch_gpa_df,
            how = 'left',
            left_on = 'semester',
            right_index = True
        )

    cleaned_emas = robust_ema_df.to_dict(orient='records')
    request.session['emas'] = json.dumps(cleaned_emas)

    robust_gpa_df = gpa_data_df.drop(columns=['branch_gpa']).merge(
        branch_gpa_df,
        how='left',
        left_on='semester',
        right_index=True
    )

    if len(branch_columns) > 1:    
        robust_gpa_df = robust_gpa_df.merge(
            branch_counts_df,
            how='left',
            left_on='semester',
            right_index=True
        )
    
        robust_gpa_df = robust_gpa_df.merge(
            branch_total_units_df,
            how='left',
            left_on='semester',
            right_index=True
        )

    ##partial correlation

    #start_time = time.time()
    partial_corr_list = []

    if len(branch_columns) > 1:
        for branch in branch_columns:
            partial_corr_list.append({
                'x': branch,
                'y': 'gpa',
                'covar': [col for col in branch_columns if col != branch]
            })
    
            partial_corr_list.append({
                'x': branch,
                'y': 'cgpa',
                'covar': [col for col in branch_columns if col != branch]
            })
    
            partial_corr_list.append({
                'x': f"{branch}_units",
                'y': 'gpa',
                'covar': [col for col in branch_columns if col != branch]
            })
    
            partial_corr_list.append({
                'x': f"{branch}_units",
                'y': 'cgpa',
                'covar': [col for col in branch_columns if col != branch]
            })
            
            partial_corr_list.append({
                'x': f"{branch}_count",
                'y': 'gpa',
                'covar': [col for col in branch_columns if col != branch]
            })
    
            partial_corr_list.append({
                'x': f"{branch}_count",
                'y': 'cgpa',
                'covar': [col for col in branch_columns if col != branch]
            })

            partial_corr_list.append({
                'x': 'semester_course_count',
                'y': 'gpa',
                'covar': ['total_units']
            })

            partial_corr_list.append({
                'x': 'semester_course_count',
                'y': 'cgpa',
                'covar': ['total_units']
            })

    partial_correlations = calculate_partial_correlations(robust_gpa_df, partial_corr_list)

    formatted_partials = []
    for (x, y), result in partial_correlations.items():
        if 'pearson' in result.index:
            formatted_partials.append({
                'x': x,
                'y': y,
                'n': result.loc['pearson', 'n'],
                'r': round(result.loc['pearson', 'r'], 6),
                'ci95': result.loc['pearson', 'CI95%'],
                'p_val': round(result.loc['pearson', 'p-val'], 6)
            })
        else:
            continue
    
    #end_time = time.time()    
    #execution_time = end_time - start_time
    #print(f"\nExecution time: {execution_time:.2f} seconds")
    
    ## correlation
    required_cor_pairs = [
        ('total_units', 'gpa'), ('total_units', 'cgpa'), 
        ('gpa', 'cgpa'), ('gpa', 'semester_course_count'),
        ('cgpa', 'semester_course_count')
    ]
    
    correlations = calculate_correlations(
        robust_gpa_df,
        column_pairs = required_cor_pairs,
    )
    
    cleaned_correlations = {str(k): str(v) for k, v in correlations.items()}
    request.session['correlations'] = json.dumps(cleaned_correlations)

    cleaned_partials = [
        {
            'x': str(partial['x']),
            'y': str(partial['y']),
            'n': int(partial['n']),
            'r': float(partial['r']),
            'p_val': float(partial['p_val'])
        }
        for partial in formatted_partials
    ]
    request.session['par_corr'] = json.dumps(cleaned_partials)

    semester_avg_scores = calculate_semester_avg_scores(cleaned_results_df)
    branch_semester_avg_scores = calculate_branch_semester_avg_scores(cleaned_results_df)

    processed_semester_data = process_gpa_data()

    return render(request, 'visual.html', {
        'processed_semester_data': processed_semester_data,
        'cleaned_results': cleaned_results,
        'gpa_data': gpa_data,
        'semester_avg_scores': semester_avg_scores,
        'branch_semester_avg_scores': branch_semester_avg_scores,
        'correlations': correlations,
        'partials': formatted_partials,
    })

def plot_view(request):
    """Displays various GPA, CGPA, and branch GPA charts, along with boxplots, scatter plots, and branch distribution charts for the student."""
    
    student, _ = get_student_from_context(request)
    if not student:
        return redirect('home:welcome')

    gpa_data = request.session.get('gpa_data_by_semester')
    semesters_gpa, gpa_values, cgpa_values = extract_combined_gpa_cgpa_data(gpa_data) if gpa_data else ([], [], [])
    
    correlations = request.session.get('correlations')
    par_corr = request.session.get('par_corr', '{}')
    emas = request.session.get('emas')

    context_corr = extract_correlations(correlations)
    if par_corr != '{}':
        context_partials = extract_partial_corr(par_corr)
        print(context_partials)
    else:
        print('There is no contextual partial correlations available')

    correlation_details = {}
    for param, value in context_corr.items():

        correlation_type, correlation_strength = get_correlation(value)
                
        correlation_details[param] = {
            'value': value,
            'type': correlation_type,
            'strength': correlation_strength
        }

    print("\nFinal correlation details:\n")
    print(correlation_details)


    branch_gpa_data = {}
    if gpa_data:
        for semester, data in gpa_data.items():
            branch_gpas = data.get('Branch_GPA', {})
            for branch, branch_gpa in branch_gpas.items():
                if branch not in branch_gpa_data:
                    branch_gpa_data[branch] = {'semesters': [], 'gpas': []}
                branch_gpa_data[branch]['semesters'].append(semester)
                branch_gpa_data[branch]['gpas'].append(branch_gpa)

    branch_gpa_chart_html = generate_branch_gpa_chart(branch_gpa_data) if branch_gpa_data else ''
    combined_chart_html = generate_combined_gpa_cgpa_chart(semesters_gpa, gpa_values, cgpa_values)

    cleaned_results_by_semester = request.session.get('cleaned_results_by_semester')
    if cleaned_results_by_semester:
        semesters, courses, units, branches, grades, scores = extract_from_cleaned_semester(cleaned_results_by_semester)

        scatter_plot_html = generate_scatter_plot(courses, scores)
        pass_rate_chart_html = generate_grouped_bar_chart_for_courses_and_pass_rate(cleaned_results_by_semester)
        semester_avg_chart, branch_avg_chart = generate_semester_score_charts(cleaned_results_by_semester, branch_colors)

        semester_avg_chart_html = semester_avg_chart.to_html(full_html=False)
        
        if len(set(branches)) > 1:
            overall_branch_pie_chart_html = generate_overall_branch_representation_pie_chart(cleaned_results_by_semester)
            semester_distribution_pie_chart_html_list = generate_branch_distribution_pie_charts(cleaned_results_by_semester)
            branch_distribution_stacked_bar_chart_html = generate_branch_distribution_stacked_bar_chart(cleaned_results_by_semester)
            branch_avg_chart_html = branch_avg_chart.to_html(full_html=False)
        else:
            overall_branch_pie_chart_html = ''
            semester_distribution_pie_chart_html_list = []
            branch_distribution_stacked_bar_chart_html = ''
            branch_avg_chart_html = ''
    else:
        scatter_plot_html = ''
        overall_branch_pie_chart_html = ''
        semester_distribution_pie_chart_html_list = []
        pass_rate_chart_html = ''
        branch_distribution_stacked_bar_chart_html = ''
        semester_avg_chart_html = ''
        branch_avg_chart_html = ''

    semester_boxplot_html, level_boxplot_html, all_scores_boxplot_html = generate_boxplot_charts(cleaned_results_by_semester)

    #display_parsed_emas(emas)

    return render(request, 'viss.html', {
        'branch_gpa_chart_html': branch_gpa_chart_html if len(set(branches)) > 1 else '',
        'combined_chart_html': combined_chart_html,
        'semester_boxplot_html': semester_boxplot_html,
        'level_boxplot_html': level_boxplot_html,
        'all_scores_boxplot_html': all_scores_boxplot_html,
        'scatter_plot_html': scatter_plot_html,
        'overall_branch_pie_chart_html': overall_branch_pie_chart_html,
        'semester_distribution_pie_chart_html_list': semester_distribution_pie_chart_html_list,
        'pass_rate_html': pass_rate_chart_html,
        'branch_distribution_stacked_bar_chart_html': branch_distribution_stacked_bar_chart_html,
        'semester_avg_chart_html': semester_avg_chart_html,
        'branch_avg_chart_html': branch_avg_chart_html,
    })
