from analyzer.results_utils import gpa_data_by_semester

def get_unique_branches(gpa_data_by_semester):
    """
    Iterate over all semesters and extract a set of unique branches present in the data.

    Args:
        gpa_data_by_semester (dict): Dictionary containing GPA, CGPA, and Branch_GPA for each semester.

    Returns:
        list: A list of unique branch names.
    """
    unique_branches = set()
    for semester, data in gpa_data_by_semester.items():
        branch_gpa = data.get('Branch_GPA', {})
        unique_branches.update(branch_gpa.keys())
    return list(unique_branches)

def ensure_all_semesters_have_all_branches(gpa_data_by_semester):
    """
    Ensure that each semester contains all unique branches. 
    If a branch is missing for a semester, insert it with the semester's CGPA as the Branch_GPA.

    Args:
        gpa_data_by_semester (dict): Dictionary containing GPA, CGPA, and Branch_GPA for each semester.

    Returns:
        dict: Updated gpa_data_by_semester where each semester has all unique branches.
    """
    unique_branches = get_unique_branches(gpa_data_by_semester)
    
    for semester, data in gpa_data_by_semester.items():
        branch_gpa = data.get('Branch_GPA', {})
        cgpa = data.get('CGPA', 0.0)
        
        for branch in unique_branches:
            if branch not in branch_gpa:
                branch_gpa[branch] = cgpa

        data['Branch_GPA'] = branch_gpa

    return gpa_data_by_semester

def extract_semester_data(gpa_data_by_semester):
    """
    Extract GPA, CGPA, and Branch_GPA for each semester.

    Args:
        gpa_data_by_semester (dict): Dictionary containing GPA, CGPA, and Branch_GPA for each semester.

    Returns:
        dict: A dictionary with the extracted GPA, CGPA, and Branch_GPA for each semester.
    """
    semester_data = {}
    for semester, data in gpa_data_by_semester.items():
        semester_data[semester] = {
            'GPA': data.get('GPA', 0.0),
            'CGPA': data.get('CGPA', 0.0),
            'Branch_GPA': data.get('Branch_GPA', {})
        }
    return semester_data

def process_gpa_data():
    """
    Main function to process the GPA data.
    1. Ensure all semesters have consistent branch data.
    2. Extract and return processed semester data.

    Returns:
        dict: A dictionary with GPA, CGPA, and Branch_GPA for each semester.
    """
    updated_gpa_data = ensure_all_semesters_have_all_branches(gpa_data_by_semester)

    processed_semester_data = extract_semester_data(updated_gpa_data)

    return processed_semester_data
