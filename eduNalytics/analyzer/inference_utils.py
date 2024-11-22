import pandas as pd
import pingouin as pg

def extract_cleaned_results_df(cleaned_results_by_semester):

    semester_keys = []
    course_codes = []
    units = []
    branches = []
    grades = []
    scores = []

    for semester, courses in cleaned_results_by_semester.items():
        for course in courses:
            semester_keys.append(semester)
            course_codes.append(course['course'])
            units.append(course['unit'])
            branches.append(course['branch'])
            grades.append(course['grade'])
            scores.append(course['score'])
    
    cleaned_results_df = pd.DataFrame({
        'semester': semester_keys,
        'course': course_codes,
        'unit': units,
        'branch': branches,
        'grade': grades,
        'score': scores
    })

    return cleaned_results_df

def count_courses_per_branch(cleaned_results_by_semester):
    branch_course_count = {}

    sorted_semesters = sorted(cleaned_results_by_semester.keys(), key=lambda x: int(x.split(' ')[0]))

    print(f"Sorted Semesters: {sorted_semesters}") 

    for semester in sorted_semesters:
        branch_counts = {}
        for course in cleaned_results_by_semester[semester]:
            branch = course['branch']
            branch_counts[branch] = branch_counts.get(branch, 0) + 1
        branch_course_count[semester] = branch_counts

    df = pd.DataFrame(branch_course_count).T.fillna(0).astype(int)
    df.index.name = "semester"

    print(f"Resulting DataFrame:\n{df}")
    return df

def extract_gpa_data_df(gpa_data_by_semester, cleaned_results_by_semester):
    semester_keys = []
    gpas = []
    branch_gpas = []
    cgpas = []
    total_units = []
    course_counts = []

    for semester, data in gpa_data_by_semester.items():
        semester_keys.append(semester)
        gpas.append(data['GPA'])
        branch_gpas.append(data['Branch_GPA'])
        cgpas.append(data['CGPA'])
        total_units.append(data['Total_units'])
        course_counts.append(len(cleaned_results_by_semester.get(semester, [])))

    gpa_data_df = pd.DataFrame({
        'semester': semester_keys,
        'gpa': gpas,
        'branch_gpa': branch_gpas,
        'cgpa': cgpas,
        'total_units': total_units,
        'semester_course_count': course_counts 
    })

    return gpa_data_df

def extract_branch_gpa_df(gpa_data_by_semester: dict):
    """
    Extracts Branch GPA data into a DataFrame for correlation analysis.

    Parameters:
    - gpa_data_by_semester (dict): Dictionary containing GPA data, including branch-specific GPAs.

    Returns:
    - pd.DataFrame: A DataFrame where rows are semesters and columns are branches.
    """
    data = []
    semesters = []

    for semester, gpa_data in gpa_data_by_semester.items():
        branch_gpas = gpa_data.get('Branch_GPA', {})
        semesters.append(semester)
        data.append(branch_gpas)

    branch_gpa_df = pd.DataFrame(data, index=semesters).fillna(0)
    branch_gpa_df.index.name = 'semester'
    
    return branch_gpa_df

def calculate_correlations(df: pd.DataFrame, column_pairs: list[tuple[str, str]], method: str = 'pearson') -> dict:
    """
    Calculate correlations between specified column pairs in a DataFrame, formatted to two decimal places as strings.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.
    - column_pairs (list of tuples): List of column pairs for which to calculate correlations.
    - method (str): The correlation method to use ('pearson', 'spearman', or 'kendall').

    Returns:
    - dict: A dictionary with column pairs as keys and their correlations as values formatted to two decimal places as strings.
    """
    correlations = {}
    for col1, col2 in column_pairs:
        if col1 in df.columns and col2 in df.columns:
            correlation = df[[col1, col2]].corr(method=method).iloc[0, 1]
            correlations[(col1, col2)] = f"{correlation:.2f}" 
        else:
            raise ValueError(f"One or both columns '{col1}' and '{col2}' are not in the DataFrame.")
    return correlations

def calculate_semester_avg_scores(df):
    """
    Calculate the average score for each semester based on all courses in that semester.
    
    Args:
        df (pd.DataFrame): DataFrame containing course data with columns for 'semester' and 'score'.
    
    Returns:
        dict: A dictionary where each semester key maps to the average score of all courses in that semester.
    """
    
    semester_avg_scores = df.groupby('semester')['score'].mean().round(1).to_dict()
    return semester_avg_scores

def calculate_branch_semester_avg_scores(df):
    """
    Calculate the average score for each branch within each semester.
    
    Args:
        df (pd.DataFrame): DataFrame containing course data with columns for 'semester', 'branch', and 'score'.
    
    Returns:
        dict: A dictionary where each semester key maps to another dictionary.
              Each inner dictionary maps branch names to their average scores.
    """
    
    grouped = df.groupby(['semester', 'branch'])['score'].mean().round(1).unstack(fill_value=0)
    
    branch_semester_avg_scores = {semester: branch_scores.dropna().to_dict() for semester, branch_scores in grouped.iterrows()}
    
    return branch_semester_avg_scores


