import pytest
import pandas as pd
from collections import defaultdict
from analyzer.inference_utils import extract_cleaned_results_df, extract_gpa_data_df

def test_extract_cleaned_results_df():
    cleaned_results_by_semester = {
        '100 level Harmattan': [
            {'course': 'ACC101', 'unit': 3, 'branch': 'Accessories', 'grade': 'B', 'score': 65},
            {'course': 'BUS101', 'unit': 3, 'branch': 'Accessories', 'grade': 'B', 'score': 60}
        ],
        '100 level Rain': [
            {'course': 'ACC102', 'unit': 3, 'branch': 'Accessories', 'grade': 'A', 'score': 74},
            {'course': 'ECO112', 'unit': 2, 'branch': 'Accessories', 'grade': 'A', 'score': 72}
        ]
    }

    expected_data = {
        'semester': ['100 level Harmattan', '100 level Harmattan', '100 level Rain', '100 level Rain'],
        'course': ['ACC101', 'BUS101', 'ACC102', 'ECO112'],
        'unit': [3, 3, 3, 2],
        'branch': ['Accessories', 'Accessories', 'Accessories', 'Accessories'],
        'grade': ['B', 'B', 'A', 'A'],
        'score': [65, 60, 74, 72]
    }
    expected_df = pd.DataFrame(expected_data)

    result_df = extract_cleaned_results_df(cleaned_results_by_semester)

    print("\n \nInput Data (cleaned_results_by_semester):")
    print(cleaned_results_by_semester)

    print("\nExpected DataFrame:")
    print(expected_df)
    
    print("\nResulting DataFrame from function:")
    print(result_df)

    pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=False)

    # Additional tests
    print("\n---- Additional Tests ----")
    # Test 1: Check if all semesters are extracted correctly
    semesters_extracted = result_df['semester'].unique()
    print("Semesters extracted:", semesters_extracted)

    assert '100 level Harmattan' in semesters_extracted
    assert '100 level Rain' in semesters_extracted
    
    # Test 2: Check if all course codes are extracted correctly
    course_codes_extracted = result_df['course'].tolist()
    print("Course codes extracted:", course_codes_extracted)

    assert set(course_codes_extracted) == set(expected_data['course'])
    
    # Test 3: Check if all units are correctly extracted
    units_extracted = result_df['unit'].tolist()
    print("Units extracted:", units_extracted)

    assert units_extracted == expected_data['unit']

    # Test 4: Check if all grades are correctly extracted
    grades_extracted = result_df['grade'].tolist()
    print("Grades extracted:", grades_extracted)

    assert grades_extracted == expected_data['grade']
    
    # Test 5: Check if all scores are correctly extracted
    scores_extracted = result_df['score'].tolist()
    print("Scores extracted:", scores_extracted)

    assert scores_extracted == expected_data['score']

def test_extract_gpa_data_df():
    
    gpa_data_by_semester = defaultdict(dict, {
        '100 level Harmattan': {'GPA': 3.9, 'Branch_GPA': {'Accessories': 3.78, 'Mathematics For Economists': 5.0}, 'CGPA': 3.9, 'Total_units': 20},
        '100 level Rain': {'GPA': 3.67, 'Branch_GPA': {'Accessories': 4.23, 'Mathematics For Economists': 0.0}, 'CGPA': 3.8, 'Total_units': 15},
        '200 level Harmattan': {'GPA': 3.18, 'Branch_GPA': {'Microeconomics': 3.0, 'Macroeconomics': 4.0, 'Accessories': 3.6, 'Mathematics For Economists': 1.5}, 'CGPA': 3.56, 'Total_units': 22},
        '200 level Rain': {'GPA': 3.91, 'Branch_GPA': {'Accessories': 4.4, 'Mathematics For Economists': 3.33, 'Microeconomics': 4.0, 'Macroeconomics': 3.0}, 'CGPA': 3.66, 'Total_units': 22},
    })
    
    expected_data = {
        'semester': ['100 level Harmattan', '100 level Rain', '200 level Harmattan', '200 level Rain'],
        'gpa': [3.9, 3.67, 3.18, 3.91],
        'branch_gpa': [
            {'Accessories': 3.78, 'Mathematics For Economists': 5.0},
            {'Accessories': 4.23, 'Mathematics For Economists': 0.0},
            {'Microeconomics': 3.0, 'Macroeconomics': 4.0, 'Accessories': 3.6, 'Mathematics For Economists': 1.5},
            {'Accessories': 4.4, 'Mathematics For Economists': 3.33, 'Microeconomics': 4.0, 'Macroeconomics': 3.0}
        ],
        'cgpa': [3.9, 3.8, 3.56, 3.66],
        'total_units': [20, 15, 22, 22]
    }
    expected_df = pd.DataFrame(expected_data)

    result_df = extract_gpa_data_df(gpa_data_by_semester)

    print("\n \nInput Data (gpa_data_by_semester):")
    print(gpa_data_by_semester)

    print("\nExpected DataFrame:")
    print(expected_df)
    
    print("\nResulting DataFrame from function:")
    print(result_df)

    pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=False)

    print("\n---- Additional Tests ----")
    # Test 1: Check if all semesters are extracted correctly
    semesters_extracted = result_df['semester'].unique()
    print("Semesters extracted:", semesters_extracted)

    assert '100 level Harmattan' in semesters_extracted
    assert '100 level Rain' in semesters_extracted
    assert '200 level Harmattan' in semesters_extracted
    assert '200 level Rain' in semesters_extracted
    
    # Test 2: Check if GPAs are extracted correctly
    gpas_extracted = result_df['gpa'].tolist()
    print("GPAs extracted:", gpas_extracted)

    assert gpas_extracted == expected_data['gpa']
    
    # Test 3: Check if Branch GPAs are extracted correctly (check the entire dictionary for branch GPAs)
    branch_gpas_extracted = result_df['branch_gpa'].tolist()
    print("Branch GPAs extracted:", branch_gpas_extracted)

    assert branch_gpas_extracted == expected_data['branch_gpa']

    # Test 4: Check if CGPAs are extracted correctly
    cgpas_extracted = result_df['cgpa'].tolist()
    print("CGPAs extracted:", cgpas_extracted)

    assert cgpas_extracted == expected_data['cgpa']

    # Test 5: Check if total units are extracted correctly
    total_units_extracted = result_df['total_units'].tolist()
    print("Total units extracted:", total_units_extracted)

    assert total_units_extracted == expected_data['total_units']

#def test_extract_combined_df():
#
#    cleaned_results_by_semester = {
#        '100 level Harmattan': [
#            {'course': 'ACC101', 'unit': 3, 'branch': 'Accessories', 'grade': 'B', 'score': 65},
#            {'course': 'BUS101', 'unit': 3, 'branch': 'Accessories', 'grade': 'B', 'score': 60}
#        ],
#        '100 level Rain': [
#            {'course': 'ACC102', 'unit': 3, 'branch': 'Accessories', 'grade': 'A', 'score': 74},
#            {'course': 'ECO112', 'unit': 2, 'branch': 'Accessories', 'grade': 'A', 'score': 72}
#        ]
#    }
#
#    gpa_data_by_semester = {
#        '100 level Harmattan': {'GPA': 3.9, 'Branch_GPA': 3.78, 'CGPA': 3.9, 'Total_units': 20},
#        '100 level Rain': {'GPA': 3.67, 'Branch_GPA': 4.23, 'CGPA': 3.8, 'Total_units': 15}
#    }
#
#    # Expected data for combined dataframe
#    expected_data = {
#        'level': ['100 level', '100 level', '100 level', '100 level'],
#        'semester': ['Harmattan', 'Harmattan', 'Rain', 'Rain'],
#        'course': ['ACC101', 'BUS101', 'ACC102', 'ECO112'],
#        'unit': [3, 3, 3, 2],
#        'branch': ['Accessories', 'Accessories', 'Accessories', 'Accessories'],
#        'grade': ['B', 'B', 'A', 'A'],
#        'score': [65, 60, 74, 72],
#        'gpa': [3.9, 3.9, 3.67, 3.67],
#        'branch_gpa': [3.78, 3.78, 4.23, 4.23],
#        'cgpa': [3.9, 3.9, 3.8, 3.8],
#        'total_units': [20, 20, 15, 15],
#    }
#    expected_df = pd.DataFrame(expected_data)
#
#    # Generate combined dataframe using function
#    combined_df = extract_combined_df(cleaned_results_by_semester, gpa_data_by_semester)
#
#    # Ensure columns are ordered the same for comparison
#    combined_df = combined_df[expected_df.columns]
#
#    print("\nExpected Combined DataFrame:")
#    print(expected_df)
#    
#    print("\nResulting Combined DataFrame from function:")
#    print(combined_df)
#
#    # Verify if the resulting DataFrame matches the expected DataFrame
#    pd.testing.assert_frame_equal(combined_df.reset_index(drop=True), expected_df, check_dtype=False, check_like=True)
#
#    # Additional Checks
#    # Test 1: Check if `level` and `semester` columns are correctly split
#    levels_extracted = combined_df['level'].unique().tolist()
#    semesters_extracted = combined_df['semester'].unique().tolist()
#
#    print("\nLevels extracted:", levels_extracted)
#    print("Semesters extracted:", semesters_extracted)
#    
#    assert '100 level' in levels_extracted
#    assert 'Harmattan' in semesters_extracted
#    assert 'Rain' in semesters_extracted
#
#    # Test 2: Check if all course codes are included
#    course_codes_extracted = combined_df['course'].tolist()
#    print("Course codes extracted:", course_codes_extracted)
#    
#    expected_courses = expected_data['course']
#    assert set(course_codes_extracted) == set(expected_courses)
#
#    # Test 3: Check if all GPA data is merged correctly
#    gpas_extracted = combined_df['gpa'].tolist()
#    print("GPAs extracted:", gpas_extracted)
#    
#    assert gpas_extracted == expected_data['gpa']
#
#    # Test 4: Verify total units from GPA data
#    total_units_extracted = combined_df['total_units'].tolist()
#    print("Total units extracted:", total_units_extracted)
#    
#    assert total_units_extracted == expected_data['total_units']
#
#    # Test 5: Verify that no columns are missing
#    expected_columns = ['course', 'unit', 'branch', 'grade', 'score', 'gpa', 'branch_gpa', 'cgpa', 'total_units', 'level', 'semester']
#    print("Combined DataFrame columns:", combined_df.columns.tolist())
#    
#    assert set(combined_df.columns) == set(expected_columns)
#
#    print("\nAll tests passed.")
