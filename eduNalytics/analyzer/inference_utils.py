import pandas as pd

def extract_cleaned_results_df(cleaned_results_by_semester):
    # Create lists to store extracted data
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
    
    # Create DataFrame
    return pd.DataFrame({
        'semester': semester_keys,
        'course': course_codes,
        'unit': units,
        'branch': branches,
        'grade': grades,
        'score': scores
    })

def extract_gpa_data_df(gpa_data_by_semester):
    # Create lists to store extracted data
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
    
    # Create DataFrame
    return pd.DataFrame({
        'semester': semester_keys,
        'gpa': gpas,
        'branch_gpa': branch_gpas,
        'cgpa': cgpas,
        'total_units': total_units
    })

def combine_semester_data(cleaned_results_df, gpa_data_df):
    # Merge the two DataFrames on 'semester' column
    combined_df = pd.merge(cleaned_results_df, gpa_data_df, on='semester', how='inner')
    
    # Split 'semester' column into 'level' and 'semester_part' columns
    combined_df[['level', 'semester']] = combined_df['semester'].str.rsplit(' ', n=1, expand=True)
    
    return combined_df