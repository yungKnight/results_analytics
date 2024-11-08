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

    print("Extracted semesters:", semesters)
    print("Extracted total units:", total_units)

    assert semesters == ['100 level Harmattan', '100 level Rain']
    assert total_units == [20, 15]

    semesters, total_units = extract_total_units({})
    print("Empty data semesters:", semesters)
    print("Empty data total units:", total_units)
    
    assert semesters == []
    assert total_units == []

def test_extract_branch_gpa_data():
    branch_gpa_data = extract_branch_gpa_data(gpa_data_sample)

    print("Extracted branch GPA data:", branch_gpa_data)

    assert 'Accessories' in branch_gpa_data
    assert 'Mathematics For Economists' in branch_gpa_data

    print("Accessories semesters:", branch_gpa_data['Accessories']['semesters'])
    print("Accessories semester GPAs:")
    for semester, gpa in zip(branch_gpa_data['Accessories']['semesters'], branch_gpa_data['Accessories']['gpas']):
        print(f"  {semester}: Accessories GPA = {gpa}")    
    print("Accessories GPAs:", branch_gpa_data['Accessories']['gpas'])

    assert branch_gpa_data['Accessories']['semesters'] == ['100 level Harmattan', '100 level Rain']
    assert branch_gpa_data['Accessories']['gpas'] == [3.78, 4.23]

    print("Mathematics For Economists semesters:", branch_gpa_data['Mathematics For Economists']['semesters'])
    print("Mathematics For Economists GPAs:", branch_gpa_data['Mathematics For Economists']['gpas'])
    assert branch_gpa_data['Mathematics For Economists']['semesters'] == ['100 level Harmattan', '100 level Rain']
    assert branch_gpa_data['Mathematics For Economists']['gpas'] == [5.0, 0.0]

    branch_gpa_data = extract_branch_gpa_data({})
    print("Extracted branch GPA data with empty input:", branch_gpa_data)
    assert branch_gpa_data == {}

def test_extract_combined_gpa_cgpa_data():
    semesters, gpas, cgpas = extract_combined_gpa_cgpa_data(gpa_data_sample)
    print("Extracted semesters:", semesters)
    print("Extracted GPAs:", gpas)
    print("Extracted CGPAs:", cgpas)

    assert semesters == ['100 level Harmattan', '100 level Rain']
    assert gpas == [3.9, 3.67]
    assert cgpas == [3.9, 3.8]

    semesters, gpas, cgpas = extract_combined_gpa_cgpa_data({})
    print("Empty data semesters:", semesters)
    print("Empty data GPAs:", gpas)
    print("Empty data CGPAs:", cgpas)
    
    assert semesters == []
    assert gpas == []
    assert cgpas == []

def test_extract_from_cleaned_semester():
    semesters, courses, units, branches, grades, scores = extract_from_cleaned_semester(cleaned_results_sample)
    print("Extracted semesters:", semesters)
    print("Extracted courses:", courses)
    print("Extracted units:", units)
    print("Extracted branches:", branches)
    print("Extracted grades:", grades)
    print("Extracted scores:", scores)

    assert semesters == ['100 level Harmattan', '100 level Rain']
    assert courses == ['ACC101', 'ECO111', 'ACC102', 'ECO114']
    assert units == [3, 2, 3, 2]
    assert branches == ['Accessories', 'Accessories', 'Accessories', 'Mathematics For Economists']
    assert grades == ['B', 'C', 'A', 'F']
    assert scores == [65, 55, 74, 21]

    semesters, courses, units, branches, grades, scores = extract_from_cleaned_semester({})
    print("Empty data semesters:", semesters)
    print("Empty data courses:", courses)
    print("Empty data units:", units)
    print("Empty data branches:", branches)
    print("Empty data grades:", grades)
    print("Empty data scores:", scores)
    
    assert semesters == []
    assert courses == []
    assert units == []
    assert branches == []
    assert grades == []
    assert scores == []

    incomplete_data = {
        '100 level Harmattan': [{'course': 'ACC101', 'unit': 3, 'branch': 'Accessories'}]
    }

    semesters, courses, units, branches, grades, scores = extract_from_cleaned_semester(incomplete_data)
    
    print("Incomplete data courses:", courses)
    print("Incomplete data units:", units)
    print("Incomplete data branches:", branches)
    print("Incomplete data grades:", grades)
    print("Incomplete data scores:", scores)
    
    assert courses == ['ACC101']
    assert units == [3]
    assert branches == ['Accessories']
    assert grades == [None]
    assert scores == [None]
