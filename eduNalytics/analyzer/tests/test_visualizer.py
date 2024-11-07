import pytest
from analyzer.visualizer_utils import (
    extract_branch_gpa_data,
    extract_combined_gpa_cgpa_data,
    extract_total_units,
    extract_from_cleaned_semester
)

gpa_data_sample = {
    '100 level Harmattan': {'GPA': 3.9, 'branches': {'Accessories': 3.78, 'Mathematics For Economists': 5.0}, 'CGPA': 3.9, 'Total_units': 20},
    '100 level Rain': {'GPA': 3.67, 'branches': {'Accessories': 4.23, 'Mathematics For Economists': 0.0}, 'CGPA': 3.8, 'Total_units': 15},
}

cleaned_results_sample = {
    '100 level Harmattan': [
        {
        'course': 'ACC101', 
        'unit': 3, 
        'branch': 'Accessories', 
        'grade': 'B', 
        'score': 65
        },

        {
        'course': 'ECO111', 
        'unit': 2, 
        'branch': 'Accessories', 
        'grade': 'C', 
        'score': 55
        },
    ],
    
    '100 level Rain': [
        {
        'course': 'ACC102', 
        'unit': 3, 
        'branch': 'Accessories', 
        'grade': 'A', 
        'score': 74
        },

        {
        'course': 'ECO114', 
        'unit': 2, 
        'branch': 'Mathematics For Economists', 
        'grade': 'F', 
        'score': 21
        },
    ],
}

def test_extract_total_units():
    
    semesters, total_units = extract_total_units(gpa_data_sample)
    assert semesters == ['100 level Harmattan', '100 level Rain']
    assert total_units == [20, 15]

    # Test with empty data
    semesters, total_units = extract_total_units({})
    assert semesters == []
    assert total_units == []

def test_extract_branch_gpa_data():
    """Test extraction of branch GPA data from gpa_data_sample."""

    branch_gpa_data = extract_branch_gpa_data(gpa_data_sample)
    print("Extracted branch GPA data:", branch_gpa_data)

    assert 'Accessories' in branch_gpa_data
    assert 'Mathematics For Economists' in branch_gpa_data
    print("Branches 'Accessories' and 'Mathematics For Economists' found in extracted data.")

    assert branch_gpa_data['Accessories']['semesters'] == ['100 level Harmattan', '100 level Rain']
    print("Accessories semesters:", branch_gpa_data['Accessories']['semesters'])
    assert branch_gpa_data['Accessories']['gpas'] == [3.78, 4.23]
    print("Accessories GPAs:", branch_gpa_data['Accessories']['gpas'])

    assert branch_gpa_data['Mathematics For Economists']['semesters'] == ['100 level Harmattan', '100 level Rain']
    print("Mathematics For Economists semesters:", branch_gpa_data['Mathematics For Economists']['semesters'])
    assert branch_gpa_data['Mathematics For Economists']['gpas'] == [5.0, 0.0]
    print("Mathematics For Economists GPAs:", branch_gpa_data['Mathematics For Economists']['gpas'])

    # Test with empty data and print results
    branch_gpa_data = extract_branch_gpa_data({})
    print("Extracted branch GPA data with empty input:", branch_gpa_data)
    assert branch_gpa_data == {}

def test_extract_combined_gpa_cgpa_data():
    
    semesters, gpas, cgpas = extract_combined_gpa_cgpa_data(gpa_data_sample)
    assert semesters == ['100 level Harmattan', '100 level Rain']
    assert gpas == [3.9, 3.67]
    assert cgpas == [3.9, 3.8]

    # Test with empty data
    semesters, gpas, cgpas = extract_combined_gpa_cgpa_data({})
    assert semesters == []
    assert gpas == []
    assert cgpas == []

def test_extract_from_cleaned_semester():
    
    semesters, courses, units, branches, grades, scores = extract_from_cleaned_semester(cleaned_results_sample)
    assert semesters == ['100 level Harmattan', '100 level Rain']
    assert courses == ['ACC101', 'ECO111', 'ACC102', 'ECO114']
    assert units == [3, 2, 3, 2]
    assert branches == ['Accessories', 'Accessories', 'Accessories', 'Mathematics For Economists']
    assert grades == ['B', 'C', 'A', 'F']
    assert scores == [65, 55, 74, 21]

    # Test with empty data
    semesters, courses, units, branches, grades, scores = extract_from_cleaned_semester({})
    assert semesters == []
    assert courses == []
    assert units == []
    assert branches == []
    assert grades == []
    assert scores == []

    # Test with missing fields in data
    incomplete_data = {
        '100 level Harmattan': [{'course': 'ACC101', 'unit': 3, 'branch': 'Accessories'}]
    }
    semesters, courses, units, branches, grades, scores = extract_from_cleaned_semester(incomplete_data)
    assert courses == ['ACC101']
    assert units == [3]
    assert branches == ['Accessories']
    assert grades == [None]
    assert scores == [None]