import pytest
from analyzer.decision_utils import extract_correlations, get_correlation

@pytest.fixture
def correlations():
    return '{"(\'total_units\', \'gpa\')": "-0.46", "(\'total_units\', \'cgpa\')": "0.11", "(\'gpa\', \'cgpa\')": "0.73", "(\'gpa\', \'semester_course_count\')": "-0.41", "(\'cgpa\', \'semester_course_count\')": "0.15"}'

def test_extract_correlations(correlations):
    """Test the extract_correlations function and correlate them with get_correlation."""

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

    assert result == expected_result, f"Expected {expected_result}, but got {result}"

    for correlation, value in result.items():
        print(f"Testing correlation: {correlation} with {value}\n")

        correlation_type, correlation_strength = get_correlation(value)
        
        print(f"Result: Type = {correlation_type}, Strength = {correlation_strength}\n")
        
        expected_type = "Positive" if value > 0 else "Negative" if value < 0 else "No Correlation"
        
        abs_value = abs(value)
        if abs_value < 0.2:
            expected_strength = "Very Weak"
        elif abs_value < 0.4:
            expected_strength = "Weak"
        elif abs_value < 0.6:
            expected_strength = "Moderate"
        elif abs_value < 0.8:
            expected_strength = "Strong"
        else:
            expected_strength = "Very Strong"
        
        assert correlation_type == expected_type, f"Expected {expected_type}, but got {correlation_type}"
        assert correlation_strength == expected_strength, f"Expected {expected_strength}, but got {correlation_strength}"

        print(f"Test passed for correlation: {correlation}\n")