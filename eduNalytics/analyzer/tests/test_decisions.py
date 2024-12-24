import pytest
import json
from analyzer.decision_utils import extract_correlations, get_correlation, extract_partial_corr, get_partial_corr_result

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

@pytest.fixture
def partial_corr_data():
    return json.dumps([
        {"x": "Accessories", "y": "gpa", "n": 8, "r": 0.933129, "p_val": 0.020549},
        {"x": "Accessories", "y": "cgpa", "n": 8, "r": 0.960561, "p_val": 0.009346},
        {"x": "Accessories_units", "y": "gpa", "n": 8, "r": -0.241435, "p_val": 0.695608},
        {"x": "Accessories_units", "y": "cgpa", "n": 8, "r": 0.10403, "p_val": 0.867784},
        {"x": "Accessories_count", "y": "gpa", "n": 8, "r": 0.242804, "p_val": 0.693918},
        {"x": "Accessories_count", "y": "cgpa", "n": 8, "r": 0.677484, "p_val": 0.208904}
    ])

def test_extract_partial_corr(partial_corr_data):
    # Print input data for debugging
    print("Input Partial Correlation Data (JSON):")
    print(partial_corr_data)

    result = extract_partial_corr(partial_corr_data)

    print("Extracted Partial Correlations Result:")
    print(result)

    expected_result = {
        ("Accessories", "gpa"): {
            "partial_corr": 0.933129,
            "prob_val": 0.020549,
            "observations": 8,
        },
        ("Accessories", "cgpa"): {
            "partial_corr": 0.960561,
            "prob_val": 0.009346,
            "observations": 8,
        },
        ("Accessories_units", "gpa"): {
            "partial_corr": -0.241435,
            "prob_val": 0.695608,
            "observations": 8,
        },
        ("Accessories_units", "cgpa"): {
            "partial_corr": 0.10403,
            "prob_val": 0.867784,
            "observations": 8,
        },
        ("Accessories_count", "gpa"): {
            "partial_corr": 0.242804,
            "prob_val": 0.693918,
            "observations": 8,
        },
        ("Accessories_count", "cgpa"): {
            "partial_corr": 0.677484,
            "prob_val": 0.208904,
            "observations": 8,
        },
    }

    assert result == expected_result, f"Expected {expected_result}, but got {result}"

    if result == expected_result:
        print("Test is successful: Extracted data matches expected output!")

    # Test the new get_partial_corr_result function
    for (x, y), data in result.items():
        r = data["partial_corr"]
        p_val = data["prob_val"]
        observations = data["observations"]

        print(f"Testing get_partial_corr_result for ({x}, {y}) with r={r}, p_val={p_val}...")

        significance, strength, correlation_type = get_partial_corr_result(r, p_val)

        print(f"Result: Significance = {significance}, Strength = {strength}, Type = {correlation_type}")

        expected_significance = (
            "Very significant" if p_val < 0.05 else
            "Significant" if p_val < 0.10 else
            "Insignificant"
        )
        
        abs_r = abs(r)
        if abs_r < 0.2:
            expected_strength = "Very Weak"
        elif abs_r < 0.4:
            expected_strength = "Weak"
        elif abs_r < 0.6:
            expected_strength = "Moderate"
        elif abs_r < 0.8:
            expected_strength = "Strong"
        else:
            expected_strength = "Very Strong"

        expected_type = "Positive" if r > 0 else "Negative" if r < 0 else "No Correlation"

        assert significance == expected_significance, f"Expected {expected_significance}, but got {significance}"
        assert strength == expected_strength, f"Expected {expected_strength}, but got {strength}"
        assert correlation_type == expected_type, f"Expected {expected_type}, but got {correlation_type}"

        print(f"Test passed for ({x}, {y})!\n")