import plotly.graph_objs as go

def extract_gpa_data(gpa_data):
    """Extract semesters and GPA values for plotting."""
    if not gpa_data:
        return [], []
    
    semesters = list(gpa_data.keys())
    gpa_values = [gpa_data[sem].get('GPA') for sem in semesters]
    return semesters, gpa_values

def extract_cgpa_data(gpa_data):
    """Extract semesters and CGPA values for plotting."""
    if not gpa_data:
        return [], []
    
    semesters = list(gpa_data.keys())
    cgpa_values = [gpa_data[sem].get('CGPA') for sem in semesters]
    return semesters, cgpa_values

def generate_gpa_chart(semesters, gpa_values):
    """Generate a GPA line chart using Plotly."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=semesters, y=gpa_values, mode='lines+markers', name='GPA'))
    fig.update_layout(
        title="GPA Time Series",
        xaxis_title="Semester",
        yaxis_title="GPA",
        template="plotly_white"
    )
    return fig.to_html(full_html=False)

def generate_cgpa_chart(semesters, cgpa_values):
    """Generate a CGPA line chart using Plotly."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=semesters, y=cgpa_values, mode='lines+markers', name='CGPA'))
    fig.update_layout(
        title="CGPA Time Series",
        xaxis_title="Semester",
        yaxis_title="CGPA",
        template="plotly_white"
    )
    return fig.to_html(full_html=False)
