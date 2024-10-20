import pytest
from unittest.mock import patch
from analyzer.advanced_utils import get_unique_branches, ensure_all_semesters_have_all_branches, extract_semester_data, process_gpa_data

@pytest.fixture
def multi_branch_scenario():
    return {
        '100 level Harmattan': {'GPA': 3.9, 'Branch_GPA': {'Accessories': 3.78, 'Mathematics For Economists': 5.0}, 'CGPA': 3.9},
        '100 level Rain': {'GPA': 3.67, 'Branch_GPA': {'Accessories': 4.23, 'Mathematics For Economists': 0.0}, 'CGPA': 3.8},
        '200 level Harmattan': {'GPA': 3.18, 'Branch_GPA': {'Microeconomics': 3.0, 'Macroeconomics': 4.0}, 'CGPA': 3.56},
        '200 level Rain': {'GPA': 3.91, 'Branch_GPA': {'Accessories': 4.4, 'Microeconomics': 3.33, 'Macroeconomics': 3.0}, 'CGPA': 3.66}
    }

def test_unique_branches(multi_branch_scenario):
    unique_branches = get_unique_branches(multi_branch_scenario)
    print(f"Unique branches: {unique_branches}")  

    assert len(unique_branches) == 4  
    assert set(unique_branches) == {'Accessories', 'Mathematics For Economists', 'Microeconomics', 'Macroeconomics'}

def test_ensure_all_semesters_have_all_branches(multi_branch_scenario):
    updated_data = ensure_all_semesters_have_all_branches(multi_branch_scenario)
    print(f"Updated data after ensuring all branches: {updated_data}")  

    for semester, data in updated_data.items():
        assert len(data['Branch_GPA']) == 4  
        assert 'Accessories' in data['Branch_GPA']
        assert 'Mathematics For Economists' in data['Branch_GPA']
        assert 'Microeconomics' in data['Branch_GPA']
        assert 'Macroeconomics' in data['Branch_GPA']

def test_extract_semester_data(multi_branch_scenario):
    semester_data = extract_semester_data(multi_branch_scenario)
    print(f"Extracted semester data: {semester_data}") 

    assert '100 level Harmattan' in semester_data
    assert semester_data['100 level Harmattan']['GPA'] == 3.9
    assert semester_data['100 level Harmattan']['CGPA'] == 3.9

def test_process_gpa_data(multi_branch_scenario):
    with patch('analyzer.advanced_utils.gpa_data_by_semester', multi_branch_scenario):
        processed_data = process_gpa_data()
    
    print(f"Processed GPA data: {processed_data}")

    assert '100 level Harmattan' in processed_data
    assert processed_data['100 level Harmattan']['GPA'] == 3.9
    assert processed_data['100 level Harmattan']['CGPA'] == 3.9

    for semester, data in processed_data.items():
        assert 'Accessories' in data['Branch_GPA']
        assert 'Mathematics For Economists' in data['Branch_GPA']
        assert 'Microeconomics' in data['Branch_GPA']
        assert 'Macroeconomics' in data['Branch_GPA']
