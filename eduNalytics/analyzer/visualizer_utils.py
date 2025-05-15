import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
import plotly.colors as pc
import random
from analyzer.inference_utils import calculate_semester_avg_scores, calculate_branch_semester_avg_scores

branch_colors = {}

def get_branch_color(branch):
    """Get color for the branch, generating a new one if not already assigned."""
    if branch not in branch_colors:
        branch_colors[branch] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return branch_colors[branch]

def extract_combined_gpa_cgpa_data(gpa_data):
    """Extract semesters, GPA, and CGPA values for plotting."""
    if not gpa_data:
        return [], [], []
    
    semesters = list(gpa_data.keys())
    gpa_values = [gpa_data[sem].get('GPA') for sem in semesters]
    cgpa_values = [gpa_data[sem].get('CGPA') for sem in semesters]
    return semesters, gpa_values, cgpa_values

def extract_from_cleaned_semester(cleaned_results_by_semester):
    """Extract values for semesters, courses, units, branches, grades, and scores respectively for plotting."""
    
    if not cleaned_results_by_semester:
        return [], [], [], [], [], []

    semesters = list(cleaned_results_by_semester.keys())
    courses, units, branches, grades, scores = [], [], [], [], []
    
    for semester in semesters:
        for course_info in cleaned_results_by_semester[semester]:
            courses.append(course_info.get('course'))
            units.append(course_info.get('unit'))
            branches.append(course_info.get('branch'))
            grades.append(course_info.get('grade'))
            scores.append(course_info.get('score'))
    
    return semesters, courses, units, branches, grades, scores

def generate_branch_gpa_data(branch_gpa_data):
    """Prepare branch GPA data for frontend rendering."""
    chart_data = []
    for branch, data in branch_gpa_data.items():
        chart_data.append({
            'name': branch,
            'semesters': data['semesters'],
            'gpas': data['gpas']
        })
    return chart_data

def generate_combined_gpa_cgpa_data(semesters, gpa_values, cgpa_values):
    """Prepare GPA and CGPA data for frontend rendering."""
    return {
        'semesters': semesters,
        'gpa': {
            'name': 'GPA',
            'values': gpa_values,
            'color': 'blue'
        },
        'cgpa': {
            'name': 'CGPA',
            'values': cgpa_values,
            'color': 'orange'
        }
    }

def generate_boxplot_data(course_data):
    """
    Generate data for boxplots for scores per semester, per level, and a combined boxplot for all courses,
    with scatter points embedded directly within the all-courses boxplot.
    
    Args:
        course_data (dict): Dictionary with semesters as keys and lists of course details as values.
        
    Returns:
        dict: JSON-serializable data structure for the three boxplot charts.
    """
    if not course_data:
        return {
            'semester_boxplot': {},
            'level_boxplot': {},
            'all_scores_boxplot': {}
        }
        
    colors = pc.qualitative.Plotly
    num_colors = len(colors)

    # Semester boxplot data
    semester_traces = []
    for i, (semester, courses) in enumerate(course_data.items()):
        scores = [course['score'] for course in courses]
        semester_traces.append({
            'type': 'box',
            'y': scores,
            'name': semester,
            'marker': {'color': colors[i % num_colors]},
            'boxmean': True,
        })
    
    semester_boxplot = {
        'data': semester_traces,
        'layout': {
            'yaxis_title': 'Scores',
            'template': 'plotly_white',
            'modebar': {
                'remove': [
                    'pan', 'zoom', 'zoomIn', 'zoomOut', 'lasso2d', 'resetScale2d'
                ]
            }
        }
    }

    # Level boxplot data
    level_scores = {}
    for semester, courses in course_data.items():
        level = semester.split(' ')[0] + " level"
        if level not in level_scores:
            level_scores[level] = []
        level_scores[level].extend([course['score'] for course in courses])

    level_traces = []
    for i, (level, scores) in enumerate(level_scores.items()):
        level_traces.append({
            'type': 'box',
            'y': scores,
            'name': level,
            'marker': {'color': colors[i % num_colors]},
            'boxmean': True
        })
    
    level_boxplot = {
        'data': level_traces,
        'layout': {
            'yaxis_title': 'Scores',
            'template': 'plotly_white',
            'modebar': {
                'remove': [
                    'pan', 'zoom', 'zoomIn', 'zoomOut', 'lasso2d', 'resetScale2d'
                ]
            }
        }
    }

    # All courses boxplot with embedded scatter points
    all_scores = [course['score'] for courses in course_data.values() for course in courses]
    all_courses_text = [f"Course: {course['course']}" for courses in course_data.values() for course in courses]

    all_scores_trace = {
        'type': 'box',
        'y': all_scores,
        'name': 'All Courses',
        'boxpoints': 'all',
        'marker': {'color': 'brown'},
        'jitter': 0.7,
        'pointpos': 0,
        'text': all_courses_text,
        'hoverinfo': 'text + y',
        'boxmean': True
    }
    
    all_scores_boxplot = {
        'data': [all_scores_trace],
        'layout': {
            'yaxis_title': 'Scores',
            'template': 'plotly_white',
            'xaxis': {
                'showticklabels': False,
                'showgrid': False
            },
            'modebar': {
                'remove': [
                    'pan', 'zoom', 'zoomIn', 'zoomOut', 'lasso2d', 'resetScale2d'
                ]
            }
        }
    }

    return {
        'semester_boxplot': semester_boxplot,
        'level_boxplot': level_boxplot,
        'all_scores_boxplot': all_scores_boxplot
    }

def prepare_scatter_plot_data(courses, scores):
    """
    Prepare raw data for a scatter plot of courses and scores.
    
    Args:
        courses (list): List of course names.
        scores (list): List of corresponding scores for each course.
        
    Returns:
        dict: JSON-serializable data structure for the scatter plot.
    """
    # Basic validation
    if not courses or not scores or len(courses) != len(scores):
        return {}
    
    # Prepare the data structure
    scatter_data = {
        'type': 'scatter',
        'data': {
            'x': courses,
            'y': scores,
            'mode': 'markers',
            'marker': {
                'size': 7,
                'color': 'red',
                'opacity': 0.6
            },
            'text': courses
        },
        'layout': {
            'yaxis_title': 'Scores',
            'template': 'plotly_white',
            'xaxis': {
                'tickangle': 60,
                'tickfont': {
                    'size': 11,
                    'style': 'italic'
                }
            },
            'modebar': {
                'remove': [
                    'pan',
                    'zoom',
                    'zoomIn',
                    'zoomOut',
                    'lasso2d',
                    'resetScale2d'
                ]
            }
        }
    }
    
    return scatter_data

def generate_overall_branch_representation_data(cleaned_results_by_semester):
    """
    Generate JSON data for overall branch representation pie chart instead of HTML.
    
    Args:
        cleaned_results_by_semester (dict): Dictionary with semesters as keys and lists of course details as values.
        
    Returns:
        dict: JSON-serializable data structure for a pie chart.
    """
    branch_counts = {}

    for semester, courses in cleaned_results_by_semester.items():
        for course_info in courses:
            branch = course_info.get('branch')
            if branch not in branch_counts:
                branch_counts[branch] = 0
            branch_counts[branch] += 1

    labels = list(branch_counts.keys())
    values = list(branch_counts.values())
    colors = [get_branch_color(branch) for branch in labels]

    # Prepare pie chart data
    pie_data = {
        'type': 'pie',
        'data': [{
            'labels': labels,
            'values': values,
            'marker': {
                'colors': colors
            }
        }],
        'layout': {
            'template': 'plotly_white',
            'margin': {
                'l': 40, 
                'r': 40, 
                't': 50, 
                'b': 5
            },
            'height': 580
        }
    }
    
    return pie_data

def generate_branch_distribution_pie_data(cleaned_results_by_semester):
    """
    Generate JSON data for branch distribution pie charts by semester.
    
    Args:
        cleaned_results_by_semester (dict): Dictionary with semesters as keys and lists of course details as values.
        
    Returns:
        list: List of pie chart data structures, one for each semester.
    """
    if not cleaned_results_by_semester:
        return []

    # Calculate branch distribution by semester
    branch_distribution = {}
    for semester, courses in cleaned_results_by_semester.items():
        branch_distribution[semester] = {}
        for course_info in courses:
            branch = course_info.get('branch')
            if branch not in branch_distribution[semester]:
                branch_distribution[semester][branch] = 0
            branch_distribution[semester][branch] += 1

    # Create pie chart data for each semester
    pie_chart_data_list = []

    for semester, distribution in branch_distribution.items():
        labels = list(distribution.keys())
        values = list(distribution.values())
        colors = [get_branch_color(branch) for branch in labels]

        pie_data = {
            'type': 'pie',
            'title': semester,
            'data': {
                'labels': labels,
                'values': values,
                'marker': {
                    'colors': colors
                }
            },
            'layout': {
                'title': semester,
                'template': 'plotly_white',
                'margin': {
                    'l': 10, 
                    'r': 20, 
                    't': 50, 
                    'b': 5
                },
                'height': 300,
                'showlegend': False
            }
        }
        pie_chart_data_list.append(pie_data)

    return pie_chart_data_list

def generate_semester_score_data(cleaned_results_by_semester, branch_colors):
    """
    Generate JSON data for semester score charts instead of Plotly chart objects.
    
    Args:
        cleaned_results_by_semester (dict): Dictionary with semesters as keys and lists of course details as values.
        branch_colors (dict): Dictionary mapping branches to colors.
        
    Returns:
        dict: JSON-serializable data structure with semester averages and branch averages.
    """
    data = []
    for semester, courses in cleaned_results_by_semester.items():
        for course in courses:
            data.append({
                'semester': semester,
                'branch': course['branch'],
                'score': course['score']
            })
    
    df = pd.DataFrame(data)
    
    semester_avg_scores = calculate_semester_avg_scores(df)
    branch_semester_avg_scores = calculate_branch_semester_avg_scores(df)

    # Prepare semester average chart data
    semester_avg_data = {
        'type': 'scatter',
        'data': {
            'x': list(semester_avg_scores.keys()),
            'y': list(semester_avg_scores.values()),
            'mode': 'lines+markers',
            'name': 'Average Score per Semester',
            'marker': {'color': 'blue'}
        },
        'layout': {
            'yaxis_title': 'Average Score',
            'modebar': {
                'remove': ['pan', 'zoom', 'zoomIn', 'zoomOut', 'lasso2d', 'resetScale2d']
            }
        }
    }
    
    # Prepare branch average chart data
    branch_avg_data = {
        'type': 'multi_scatter',
        'data': [],
        'layout': {
            'yaxis_title': 'Average Score',
            'legend_title': 'Branches',
            'modebar': {
                'remove': ['pan', 'zoom', 'zoomIn', 'zoomOut', 'lasso2d', 'resetScale2d']
            }
        }
    }
    
    # Add traces for each branch
    for branch, color in branch_colors.items():
        # Only include branches that have actual data
        branch_data = {}
        for semester, branches in branch_semester_avg_scores.items():
            if branch in branches:
                branch_data[semester] = branches[branch]
                
        if not branch_data:
            continue
            
        # Create x and y values only for semesters where this branch has data
        semesters = list(branch_data.keys())
        scores = list(branch_data.values())
        
        branch_avg_data['data'].append({
            'x': semesters,
            'y': scores,
            'mode': 'lines+markers',
            'name': branch,
            'marker': {'color': color},
            'connectgaps': True
        })
    
    return {
        'semester_avg': semester_avg_data,
        'branch_avg': branch_avg_data
    }

def generate_courses_and_pass_rate_data(cleaned_results_by_semester):
    """
    Generate raw data for courses and pass rate by branch and semester.
    This optimized version only prepares the data structure, not the chart.

    Args:
        cleaned_results_by_semester (dict): Dictionary with semesters as keys and lists of course details as values.

    Returns:
        dict: Structured data for frontend pass rate visualization.
    """
    # Process the data
    branch_data = {}
    all_branches = set()

    for semester, courses in cleaned_results_by_semester.items():
        total_courses_per_branch = {}
        passed_courses_per_branch = {}

        for course in courses:
            branch = course['branch']
            all_branches.add(branch)
            total_courses_per_branch[branch] = total_courses_per_branch.get(branch, 0) + 1
            if course['score'] >= 40:
                passed_courses_per_branch[branch] = passed_courses_per_branch.get(branch, 0) + 1

        branch_data[semester] = {
            'total': total_courses_per_branch,
            'passed': passed_courses_per_branch
        }

    # Define branch colors - maintaining your color scheme
    predefined_colors = ['#FF6347', '#FFD700', '#1E90FF', '#32CD32', '#FF69B4', '#8A2BE2']
    branch_colors = {branch: predefined_colors[i % len(predefined_colors)] for i, branch in enumerate(sorted(all_branches))}
    
    result = {
        'semesters': list(branch_data.keys()),
        'branches': {
            branch: {
                'color': branch_colors[branch],
                'total': [branch_data.get(semester, {}).get('total', {}).get(branch, 0) for semester in branch_data],
                'passed': [branch_data.get(semester, {}).get('passed', {}).get(branch, 0) for semester in branch_data]
            }
            for branch in all_branches
        },
        'chart_settings': {
            'barmode': 'group',
            'yaxis_title': 'Number of Courses',
            'plot_bgcolor': '#ffffcc',
            'height': 500
        }
    }
    
    return result

def generate_branch_distribution_data(cleaned_results_by_semester):
    """
    Generate data for a stacked bar chart to show the branch distribution per semester.

    Args:
        cleaned_results_by_semester (dict): Dictionary with semesters as keys and lists of course details as values.

    Returns:
        dict: Data structure for creating a stacked bar chart on the frontend.
    """
    predefined_colors = ['#FF6347', '#FFD700', '#1E90FF', '#32CD32', '#FF69B4', '#8A2BE2']
    
    # Calculate branch course count per semester
    branch_course_count_per_semester = {}
    all_branches = set()

    for semester, courses in cleaned_results_by_semester.items():
        branch_course_count_per_semester[semester] = {}
        for course in courses:
            branch = course['branch']
            all_branches.add(branch)
            if branch not in branch_course_count_per_semester[semester]:
                branch_course_count_per_semester[semester][branch] = 0
            branch_course_count_per_semester[semester][branch] += 1

    # Assign colors to branches
    branch_colors = {}
    for i, branch in enumerate(sorted(all_branches)):
        branch_colors[branch] = predefined_colors[i % len(predefined_colors)]
    
    # Prepare data for frontend
    semesters = list(branch_course_count_per_semester.keys())
    branches_data = []
    
    for branch, color in branch_colors.items():
        branch_counts = [
            branch_course_count_per_semester[semester].get(branch, 0) 
            for semester in semesters
        ]
        
        branches_data.append({
            'name': branch,
            'counts': branch_counts,
            'color': color
        })
    
    # Return structured data for frontend
    return {
        'semesters': semesters,
        'branches': branches_data,
        'layout': {
            'yaxis_title': 'Number of Courses',
            'template': 'plotly_white',
            'height': 500,
            'barmode': 'stack',
            'bargap': 0.4
        }
    }
