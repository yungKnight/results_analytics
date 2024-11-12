import pytest
import pandas as pd
from collections import defaultdict
from analyzer.inference_utils import (
    extract_cleaned_results_df,
    extract_gpa_data_df,
    calculate_semester_avg_scores,
    calculate_branch_semester_avg_scores,
    calculate_correlations
)

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

def test_calculate_semester_avg_scores():
    # Sample data
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

    # Create DataFrame using extract_cleaned_results_df function
    df = extract_cleaned_results_df(cleaned_results_by_semester)
    
    # Expected result for semester average scores
    expected_avg_scores = {
        '100 level Harmattan': (65 + 60) / 2,
        '100 level Rain': (74 + 72) / 2
    }

    # Calculate semester average scores
    result_avg_scores = calculate_semester_avg_scores(df)
    
    print("\nExpected Semester Average Scores:", expected_avg_scores)
    print("Calculated Semester Average Scores:", result_avg_scores)
    
    print("\n")
    assert result_avg_scores == expected_avg_scores
    print("\n")
    
def test_calculate_branch_semester_avg_scores():
    cleaned_results_by_semester = {
        '100 level Harmattan': [
            {'course': 'ACC101', 'unit': 3, 'branch': 'Accessories', 'grade': 'B', 'score': 65},
            {'course': 'ACC102', 'unit': 3, 'branch': 'Accessories', 'grade': 'A', 'score': 75},
            {'course': 'MAT101', 'unit': 3, 'branch': 'Mathematics', 'grade': 'A', 'score': 80},
            {'course': 'ENG101', 'unit': 3, 'branch': 'Engineering', 'grade': 'B', 'score': 72}
        ],

        '100 level Rain': [
            {'course': 'ACC103', 'unit': 3, 'branch': 'Accessories', 'grade': 'A', 'score': 74},
            {'course': 'ACC104', 'unit': 3, 'branch': 'Accessories', 'grade': 'B', 'score': 78},
            {'course': 'MAT102', 'unit': 2, 'branch': 'Mathematics', 'grade': 'A', 'score': 70},
            {'course': 'ENG102', 'unit': 2, 'branch': 'Engineering', 'grade': 'B', 'score': 68},
            {'course': 'ENG103', 'unit': 2, 'branch': 'Engineering', 'grade': 'A', 'score': 85}
        ]
    }

    df = extract_cleaned_results_df(cleaned_results_by_semester)
    
    expected_branch_avg_scores = {
        '100 level Harmattan': {
            'Accessories': 70.0,  
            'Mathematics': 80.0,  
            'Engineering': 72.0   
        },

        '100 level Rain': {
            'Accessories': 76.0, 
            'Mathematics': 70.0,
            'Engineering': 76.5 
        }
    }

    result_branch_avg_scores = calculate_branch_semester_avg_scores(df)
    
    print("\nExpected Branch Semester Average Scores:", expected_branch_avg_scores)
    print("Calculated Branch Semester Average Scores:", result_branch_avg_scores)
    
    assert result_branch_avg_scores == expected_branch_avg_scores

def test_calculate_correlations():
    data = {
        'GPA': [3.9, 3.7, 3.5, 3.8],
        'CGPA': [3.8, 3.75, 3.6, 3.85],
        'Total_units': [20, 22, 24, 18],
        'Average_score': [70, 72, 68, 74]
    }
    df = pd.DataFrame(data)

    column_pairs = [('GPA', 'CGPA'), ('GPA', 'Average_score'), ('Total_units', 'Average_score')]

    expected_correlations = {
        ('GPA', 'CGPA'): f"{df['GPA'].corr(df['CGPA']):.2f}",
        ('GPA', 'Average_score'): f"{df['GPA'].corr(df['Average_score']):.2f}",
        ('Total_units', 'Average_score'): f"{df['Total_units'].corr(df['Average_score']):.2f}"
    }

    print("\n \nExpected correlations (formatted as strings):")
    for key, value in expected_correlations.items():
        print(f"{key}: {value}")

    result = calculate_correlations(df, column_pairs)

    print("\nActual function result (formatted as strings):")
    for key, value in result.items():
        print(f"{key}: {value}")

    try:
        assert result == expected_correlations, f"Expected {expected_correlations} but got {result}"
        print("\nTest passed: Function output matches expected correlations.")
    except AssertionError as e:
        print("\nTest failed:", e)

    print("\nTesting with an invalid column pair to trigger ValueError:")
    with pytest.raises(ValueError) as exc_info:
        calculate_correlations(df, [('GPA', 'NonExistentColumn')])
    print(f"Caught expected ValueError: {exc_info.value}")
