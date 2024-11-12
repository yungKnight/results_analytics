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

def extract_gpa_data_df(gpa_data_by_semester):

    semester_keys = []
    gpas = []
    branch_gpas = []
    cgpas = []
    total_units = []

    for semester, data in gpa_data_by_semester.items():
        semester_keys.append(semester)
        gpas.append(data['GPA'])
        branch_gpas.append(data['Branch_GPA'])
        cgpas.append(data['CGPA'])
        total_units.append(data['Total_units'])

    gpa_data_df= pd.DataFrame({
        'semester': semester_keys,
        'gpa': gpas,
        'branch_gpa': branch_gpas,
        'cgpa': cgpas,
        'total_units': total_units
    })

    return gpa_data_df

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
            correlations[(col1, col2)] = f"{correlation:.2f}"  # Format to two decimal places as a string
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
    
    semester_avg_scores = df.groupby('semester')['score'].mean().to_dict()
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
    
    grouped = df.groupby(['semester', 'branch'])['score'].mean().unstack(fill_value=0)
    
    branch_semester_avg_scores = {semester: branch_scores.dropna().to_dict() for semester, branch_scores in grouped.iterrows()}
    
    return branch_semester_avg_scores


