import pytest
from analyzer.decision_utils import extract_correlations

@pytest.fixture
def correlations():
    return '{"(\'total_units\', \'gpa\')": "-0.46", "(\'total_units\', \'cgpa\')": "0.11", "(\'gpa\', \'cgpa\')": "0.73", "(\'gpa\', \'semester_course_count\')": "-0.41", "(\'cgpa\', \'semester_course_count\')": "0.15"}'

def test_extract_correlations(correlations):
    print("Testing with correlations context:")
    print(correlations)

    result = extract_correlations(correlations)

    print("Extracted correlations result:")
    print(result)

    expected_result = {
        ('total_units', 'gpa'): -0.46,
        ('total_units', 'cgpa'): 0.11,
        ('gpa', 'cgpa'): 0.73,
        ('gpa', 'semester_course_count'): -0.41,
        ('cgpa', 'semester_course_count'): 0.15,
    }

    print(expected_result)

    assert result == expected_result, f"Expected {expected_result}, but got {result}"

    if result == expected_result:
        print("Test is successful")