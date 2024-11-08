import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.colors as pc
import random

branch_colors = {}

def get_branch_color(branch):
    """Get color for the branch, generating a new one if not already assigned."""
    if branch not in branch_colors:
        branch_colors[branch] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return branch_colors[branch]

def extract_total_units(gpa_data):
    """Extract semesters and total units values for plotting."""
    if not gpa_data:
        return [], []
    
    semesters = list(gpa_data.keys())
    total_units = [gpa_data[sem].get('Total_units', 0) for sem in semesters]
    return semesters, total_units

def extract_branch_gpa_data(gpa_data):
    """Extract semesters and branch GPAs from gpa_data."""
    branch_gpa_by_semester = {}

    if gpa_data:
        for semester, semester_data in gpa_data.items():
            branches = semester_data.get('branches', {})
            for branch, branch_gpa in branches.items():
                if branch not in branch_gpa_by_semester:
                    branch_gpa_by_semester[branch] = {'semesters': [], 'gpas': []}
                
                branch_gpa_by_semester[branch]['semesters'].append(semester)
                branch_gpa_by_semester[branch]['gpas'].append(branch_gpa)
    
    return branch_gpa_by_semester

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

def extract_passed_courses_from_cleaned_semester(cleaned_results_by_semester):
    """Extract values for semesters, courses, units, branches, grades, and scores for passed courses (score >= 40)."""
    
    if not cleaned_results_by_semester:
        return [], [], [], [], [], []

    semesters = list(cleaned_results_by_semester.keys())
    courses, units, branches, grades, scores = [], [], [], [], []
    
    for semester in semesters:
        for course_info in cleaned_results_by_semester[semester]:
            if course_info.get('score', 0) >= 40:
                courses.append(course_info.get('course'))
                units.append(course_info.get('unit'))
                branches.append(course_info.get('branch'))
                grades.append(course_info.get('grade'))
                scores.append(course_info.get('score'))
    
    return semesters, courses, units, branches, grades, scores

def generate_branch_gpa_chart(branch_gpa_data):
    """Generate a time series chart for each branch GPA."""
    fig = go.Figure()

    for branch, data in branch_gpa_data.items():
        fig.add_trace(go.Scatter(
            x=data['semesters'],
            y=data['gpas'],
            mode='lines+markers',
            name=branch
        ))

    fig.update_layout(
        modebar=dict(
            remove=[
            "pan",               
            "zoom",              
            "zoomIn",            
            "zoomOut",           
            "lasso2d",
            "resetScale2d",
            ]
        ),
        xaxis_title="Semester",
        yaxis_title="GPA",
        template="plotly_white"
    )
    return fig.to_html(full_html=False)

def generate_combined_gpa_cgpa_chart(semesters, gpa_values, cgpa_values):
    """Generate a combined GPA and CGPA time series chart using Plotly."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=semesters,
        y=gpa_values,
        mode='lines+markers',
        name='GPA',
        line=dict(color='blue'),
    ))

    fig.add_trace(go.Scatter(
        x=semesters,
        y=cgpa_values,
        mode='lines+markers',
        name='CGPA',
        line=dict(color='orange'),
    ))

    fig.update_layout(
        modebar=dict(
            remove=[
            "pan",               
            "zoom",              
            "zoomIn",            
            "zoomOut",           
            "lasso2d",
            "resetScale2d",
            ]
        ),
        xaxis_title="Semester",
        yaxis_title="Value",
        template="plotly_white",
    )
    return fig.to_html(full_html=False)

def generate_boxplot_charts(course_data):
    """
    Generate boxplots for scores per semester, per level, and a combined boxplot for all courses,
    with scatter points embedded directly within the all-courses boxplot.
    
    Args:
        course_data (dict): Dictionary with semesters as keys and lists of course details as values.
        
    Returns:
        tuple: HTML strings for per-semester, per-level, and all-course boxplot figures.
    """
    semester_fig = go.Figure()
    level_fig = go.Figure()
    all_scores_fig = go.Figure()

    colors = pc.qualitative.Plotly
    num_colors = len(colors)

    for i, (semester, courses) in enumerate(course_data.items()):
        scores = [course['score'] for course in courses]
        semester_fig.add_trace(go.Box(
            y=scores,
            name=semester,
            marker=dict(color=colors[i % num_colors]),
            boxmean=True,
            median=('blue', 2, 'dot', 0.6)
        ))

    semester_fig.update_layout(
        modebar=dict(
            remove=[
            "pan",               
            "zoom",              
            "zoomIn",            
            "zoomOut",           
            "lasso2d",
            "resetScale2d",
            ]
        ),
        yaxis_title="Scores",
        template="plotly_white"
    )

    level_scores = {}
    for semester, courses in course_data.items():
        level = semester.split(' ')[0] + " level"
        if level not in level_scores:
            level_scores[level] = []
        level_scores[level].extend([course['score'] for course in courses])

    for i, (level, scores) in enumerate(level_scores.items()):
        level_fig.add_trace(go.Box(
            y=scores,
            name=level,
            marker=dict(color=colors[i % num_colors]),
            boxmean=True,
        ))

    level_fig.update_layout(
        modebar=dict(
            remove=[
            "pan",               
            "zoom",              
            "zoomIn",            
            "zoomOut",           
            "lasso2d",
            "resetScale2d",
            ]
        ),
        yaxis_title="Scores",
        template="plotly_white"
    )

    all_scores = [course['score'] for courses in course_data.values() for course in courses]
    all_courses_text = [f"Course: {course['course']}" for courses in course_data.values() for course in courses]

    all_scores_fig.add_trace(go.Box(
        y=all_scores,
        name="All Courses",
        boxpoints="all",  
        marker_color='brown',
        jitter=0.7, 
        pointpos=0,
        text=all_courses_text,
        hoverinfo="text + y",
        boxmean=True,
    ))
    
    all_scores_fig.update_layout(
        modebar=dict(
            remove=[
            "pan",               
            "zoom",              
            "zoomIn",            
            "zoomOut",           
            "lasso2d",
            "resetScale2d",
            ]
        ),
        yaxis_title="Scores",
        xaxis=dict(
            showticklabels=False,
            showgrid=False
        ),
        template="plotly_white"
    )

    return (
        semester_fig.to_html(full_html=False),
        level_fig.to_html(full_html=False),
        all_scores_fig.to_html(full_html=False)
    )

def generate_scatter_plot(courses, scores):
    """
    Generate a scatter plot for courses and scores.
    
    Args:
        courses (list): List of course names.
        scores (list): List of corresponding scores for each course.
        
    Returns:
        str: HTML string for the scatter plot figure.
    """
    scatter_fig = go.Figure()

    scatter_fig.add_trace(go.Scatter(
        x=courses,
        y=scores,
        mode='markers',
        marker=dict(size=7, color='red', opacity=0.6),
        text=courses
    ))

    scatter_fig.update_layout(
        modebar=dict(
            remove=[
            "pan",               
            "zoom",              
            "zoomIn",            
            "zoomOut",           
            "lasso2d",
            "resetScale2d",
            ]
        ),
        xaxis_title="Courses",
        yaxis_title="Scores",
        template="plotly_white",
        xaxis=dict(tickangle=60, tickfont=dict(size=11, style="italic"))
    )

    return scatter_fig.to_html(full_html=False)

def generate_overall_branch_representation_pie_chart(cleaned_results_by_semester):
    """Generate a pie chart showing the overall representation of branches."""
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

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=5),
        height=580
    )

    return fig.to_html(full_html=False)

def generate_branch_distribution_pie_charts(cleaned_results_by_semester):
    """Generate individual pie charts for branch distribution of courses per semester."""
    if not cleaned_results_by_semester:
        return []

    branch_distribution = {}
    for semester, courses in cleaned_results_by_semester.items():
        branch_distribution[semester] = {}
        for course_info in courses:
            branch = course_info.get('branch')
            if branch not in branch_distribution[semester]:
                branch_distribution[semester][branch] = 0
            branch_distribution[semester][branch] += 1

    pie_chart_html_list = []

    for semester, distribution in branch_distribution.items():
        labels = list(distribution.keys())
        values = list(distribution.values())
        colors = [get_branch_color(branch) for branch in labels]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
        fig.update_layout(
            title_text=f'{semester}', 
            template="plotly_white",
            margin=dict(l=10, r=20, t=50, b=5),
            height=300,
            showlegend=False
        )
        
        pie_chart_html_list.append(fig.to_html(full_html=False))

    return pie_chart_html_list

def generate_grouped_bar_chart_for_courses_and_pass_rate(cleaned_results_by_semester):
    """
    Generate a grouped bar chart that combines total courses per branch and passed courses per branch
    to show the pass rate for each branch in a semester.

    Args:
        cleaned_results_by_semester (dict): Dictionary with semesters as keys and lists of course details as values.

    Returns:
        str: HTML string for the grouped bar chart.
    """

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

    predefined_colors = ['#FF6347', '#FFD700', '#1E90FF', '#32CD32', '#FF69B4', '#8A2BE2']
    branch_colors = {branch: predefined_colors[i % len(predefined_colors)] for i, branch in enumerate(sorted(all_branches))}

    fig = go.Figure()

    for branch, color in branch_colors.items():
        total_courses = [branch_data.get(semester, {}).get('total', {}).get(branch, 0) for semester in branch_data]
        passed_courses = [branch_data.get(semester, {}).get('passed', {}).get(branch, 0) for semester in branch_data]

        fig.add_trace(go.Bar(
            name=f"{branch} offered",
            x=list(branch_data.keys()),
            y=total_courses,
            marker_color=color,
            opacity=1.0 
        ))

        fig.add_trace(go.Bar(
            name=f"Passed {branch}",
            x=list(branch_data.keys()),
            y=passed_courses,
            marker_color=color,
            opacity=0.55
        ))

    fig.update_layout(
        barmode='group',
        modebar=dict(
            remove=[
            "pan",               
            "zoom",              
            "zoomIn",            
            "zoomOut",           
            "lasso2d",
            "resetScale2d",
            ]
        ),
        xaxis_title="Semester",
        yaxis_title="Number of Courses",
        template="plotly_white",
        xaxis=dict(tickangle=45, tickfont=dict(
            style="italic"
            )
        ),
        plot_bgcolor = "#ffffcc",
        height=500,
    )

    return fig.to_html(full_html=False)

def generate_branch_distribution_stacked_bar_chart(cleaned_results_by_semester):
    """
    Generate a stacked bar chart to show the branch distribution per semester.

    Args:
        cleaned_results_by_semester (dict): Dictionary with semesters as keys and lists of course details as values.

    Returns:
        str: HTML string for the stacked bar chart.
    """
    
    predefined_colors = ['#FF6347', '#FFD700', '#1E90FF', '#32CD32', '#FF69B4', '#8A2BE2']
    branch_colors = {} 

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

    for i, branch in enumerate(sorted(all_branches)):
        branch_colors[branch] = predefined_colors[i % len(predefined_colors)]

    fig = go.Figure()

    for branch, color in branch_colors.items():
        branch_counts = [
            branch_course_count_per_semester[semester].get(branch, 0) 
            for semester in branch_course_count_per_semester.keys()
        ]
        
        fig.add_trace(go.Bar(
            name=branch,

            x=list(branch_course_count_per_semester.keys()),
            y=branch_counts,
            marker_color=color
        ))

    fig.update_layout(
        barmode='stack',
        xaxis_title="Semester",
        yaxis_title="Number of Courses",
        template="plotly_white",
        height=500,
        modebar=dict(
            remove=[
            "pan",               
            "zoom",              
            "zoomIn",            
            "zoomOut",           
            "lasso2d",
            "resetScale2d",
            ]
        ),
        bargap=0.4,
    )

    return fig.to_html(full_html=False)