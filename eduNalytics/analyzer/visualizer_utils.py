import plotly.graph_objs as go

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


def generate_branch_gpa_chart(branch_gpa_data):
    """Generate a time series chart for each branch GPA."""
    fig = go.Figure()

    for branch, data in branch_gpa_data.items():
        fig.add_trace(go.Scatter(
            x=data['semesters'],
            y=data['gpas'],
            mode='lines+markers',
            name=f'Branch: {branch}'
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
        template="plotly_white"
    )
    return fig.to_html(full_html=False)
