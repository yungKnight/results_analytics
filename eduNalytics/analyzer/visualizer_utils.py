import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.colors as pc

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
            marker=dict(color=colors[i % num_colors])
        ))

    semester_fig.update_layout(
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
            marker=dict(color=colors[i % num_colors])
        ))

    level_fig.update_layout(
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
        hoverinfo="text + y" 
    ))
    
    all_scores_fig.update_layout(
        title="Boxplot with Built-in Points",
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
        xaxis_title="Courses",
        yaxis_title="Scores",
        template="plotly_white",
        xaxis=dict(tickangle=60, tickfont=dict(size=11, style="italic"))
    )

    return scatter_fig.to_html(full_html=False)



def generate_branch_course_frequency_charts(cleaned_results_by_semester):
    """
    Generates pie charts showing course frequency per branch for each semester.
    
    Args:
        cleaned_results_by_semester (dict): Data containing branch, grade, and course details by semester.
    
    Returns:
        dict: A dictionary with Plotly figure objects for the charts.
    """
    figs = {}

    # Loop through each semester to create course frequency pie charts
    for semester, courses in cleaned_results_by_semester.items():
        # Calculate data for course frequency per branch
        branch_counts = {}
        for course in courses:
            branch = course.get('branch')
            branch_counts[branch] = branch_counts.get(branch, 0) + 1
        
        # Generate course frequency pie chart for this semester
        fig = go.Figure()
        fig.add_trace(
            go.Pie(
                labels=list(branch_counts.keys()),
                values=list(branch_counts.values()),
                name=f"Course Frequency for {semester}",
                textinfo="label+percent"
            )
        )
        fig.update_layout(title_text=f"Course Frequency for {semester}")
        
        # Store the figure in the dictionary
        figs[semester] = fig

    return figs

def generate_overall_course_frequency_chart(cleaned_results_by_semester):
    """
    Generates a single pie chart that shows the overall course frequency across all semesters.
    
    Args:
        cleaned_results_by_semester (dict): Data containing branch, grade, and course details by semester.
    
    Returns:
        str: HTML string for the overall course frequency pie chart.
    """
    overall_branch_counts = {}

    # Aggregate data for course frequency across all semesters
    for courses in cleaned_results_by_semester.values():
        for course in courses:
            branch = course.get('branch')
            overall_branch_counts[branch] = overall_branch_counts.get(branch, 0) + 1
    
    # Generate the overall course frequency pie chart
    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            labels=list(overall_branch_counts.keys()),
            values=list(overall_branch_counts.values()),
            textinfo="label+percent"
        )
    )
    fig.update_layout(title_text="Overall Course Frequency Across Semesters")
    
    return fig.to_html(full_html=False)