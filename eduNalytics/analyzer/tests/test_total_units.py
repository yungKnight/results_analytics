import pytest
from collections import defaultdict
from analyzer.results_utils import calculate_total_units_for_semester, cleaned_results_by_semester, gpa_data_by_semester
from unittest.mock import Mock

@pytest.fixture
def mock_course_results():
    """Fixture to provide mock course results for testing."""
    result1 = Mock()
    result1.unit = 3
    result1.level = '100'
    result1.course = 'Course 101'
    
    result2 = Mock()
    result2.unit = 4
    result2.level = '100'
    result2.course = 'Course 102'

    result3 = Mock()
    result3.unit = None
    result3.level = '200'
    result3.course = 'Course 201'

    result4 = Mock()
    result4.unit = 3
    result4.level = '200'
    result4.course = 'Course 202'

    result5 = Mock()
    result5.unit = 3
    result5.level = '100'
    result5.course = 'Course 103'
    
    result6 = Mock()
    result6.unit = 4
    result6.level = '100'
    result6.course = 'Course 104'

    result7 = Mock()
    result7.unit = None
    result7.level = '200'
    result7.course = 'Course 203'

    result8 = Mock()
    result8.unit = 3
    result8.level = '200'
    result8.course = 'Course 204'

    cleaned_results_by_semester['100 level Harmattan'] = [result1, result5]
    cleaned_results_by_semester['100 level Rain'] = [result2, result6]
    cleaned_results_by_semester['200 level Rain'] = [result4, result8]
    cleaned_results_by_semester['200 level Harmattan'] = [result3, result7]

    return cleaned_results_by_semester

def test_calculate_total_units_for_semester(mock_course_results):
    """Test the calculate_total_units_for_semester function."""
    assert len(cleaned_results_by_semester) > 0

    # Call the function
    gpa_data_by_semester.clear()
    calculate_total_units_for_semester()

    assert gpa_data_by_semester['100 level Harmattan']['Total_units'] < 7

    assert gpa_data_by_semester['200 level Harmattan']['Total_units'] == 4

    assert gpa_data_by_semester['100 level Rain']['Total_units'] > 7

    assert gpa_data_by_semester['200 level Rain']['Total_units'] == 6 

    assert 'Total_units' in gpa_data_by_semester['100 level Harmattan']
    assert 'Total_units' in gpa_data_by_semester['200 level Harmattan']
