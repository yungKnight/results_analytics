import pytest
import json
from analyzer.decision_utils import (
        extract_correlations, get_correlation, extract_partial_corr, 
        get_partial_corr_result, extract_emas, get_results_from_emas, extract_needed_data
    )

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

@pytest.fixture
def example_emas_data():
    return json.dumps([
        {"semester": "100 level Harmattan", "gpa": 3.9, "cgpa": 3.9, "gpa_ema": 3.9, "cgpa_ema": 3.9, 
         "Accessories": 3.78, "Mathematics For Economists": 5.0, "Microeconomics": 0.0, "Macroeconomics": 0.0},
        {"semester": "100 level Rain", "gpa": 3.67, "cgpa": 3.8, "gpa_ema": 3.81, "cgpa_ema": 3.86, 
         "Accessories": 4.23, "Mathematics For Economists": 0.0, "Microeconomics": 0.0, "Macroeconomics": 0.0},
        {"semester": "200 level Harmattan", "gpa": 3.18, "cgpa": 3.56, "gpa_ema": 3.56, "cgpa_ema": 3.74, 
         "Accessories": 3.6, "Mathematics For Economists": 1.5, "Microeconomics": 3.0, "Macroeconomics": 4.0},
        {"semester": "200 level Rain", "gpa": 3.91, "cgpa": 3.66, "gpa_ema": 3.7, "cgpa_ema": 3.71, 
         "Accessories": 4.4, "Mathematics For Economists": 3.33, "Microeconomics": 4.0, "Macroeconomics": 3.0},
        {"semester": "300 level Harmattan", "gpa": 1.69, "cgpa": 3.17, "gpa_ema": 2.89, "cgpa_ema": 3.49, 
         "Accessories": 2.0, "Mathematics For Economists": 1.0, "Microeconomics": 1.0, "Macroeconomics": 2.0},
        {"semester": "300 level Rain", "gpa": 1.9, "cgpa": 2.97, "gpa_ema": 2.5, "cgpa_ema": 3.28, 
         "Accessories": 2.5, "Mathematics For Economists": 0.5, "Microeconomics": 2.0, "Macroeconomics": 2.0},
        {"semester": "400 level Harmattan", "gpa": 1.82, "cgpa": 2.8, "gpa_ema": 2.23, "cgpa_ema": 3.09, 
         "Accessories": 1.67, "Mathematics For Economists": 2.0, "Microeconomics": 3.0, "Macroeconomics": 1.67},
        {"semester": "400 level Rain", "gpa": 3.4, "cgpa": 2.83, "gpa_ema": 2.7, "cgpa_ema": 2.99, 
         "Accessories": 3.0, "Mathematics For Economists": 0.0, "Microeconomics": 4.0, "Macroeconomics": 3.5}
    ])


def test_extract_emas(example_emas_data):
    print("\nTesting extract_emas function...")

    result = extract_emas(example_emas_data)
    print("Function result successfully retrieved.")

    print("Validating extracted data for '100 level Harmattan'...")
    assert "100 level Harmattan" in result
    assert result["100 level Harmattan"]["gpa"] == 3.9
    assert result["100 level Harmattan"]["cgpa"] == 3.9
    assert result["100 level Harmattan"]["gpa_ema"] == 3.9
    assert result["100 level Harmattan"]["cgpa_ema"] == 3.9
    assert result["100 level Harmattan"]["user_specific_params"] == {
        "Accessories": 3.78,
        "Mathematics For Economists": 5.0,
        "Microeconomics": 0.0,
        "Macroeconomics": 0.0
    }
    print("Validation for '100 level Harmattan' passed.")

    print("Validating extracted data for '300 level Harmattan'...")
    assert "300 level Harmattan" in result
    assert result["300 level Harmattan"]["gpa"] == 1.69
    assert result["300 level Harmattan"]["cgpa"] == 3.17
    assert result["300 level Harmattan"]["gpa_ema"] == 2.89
    assert result["300 level Harmattan"]["cgpa_ema"] == 3.49
    assert result["300 level Harmattan"]["user_specific_params"] == {
        "Accessories": 2.0,
        "Mathematics For Economists": 1.0,
        "Microeconomics": 1.0,
        "Macroeconomics": 2.0
    }
    print("Validation for '300 level Harmattan' passed.")

    print("Validating total number of semesters...")
    assert len(result) == 8  
    print("Total semesters validation passed.")

    print("Validating dynamically generated parameters for each semester...")
    for semester, data in result.items():
        assert "user_specific_params" in data
        assert isinstance(data["user_specific_params"], dict)
        print(f"Dynamic parameters for '{semester}' validated successfully.")

    print("All tests for extract_emas passed successfully.")

    print("\nExtending tests to validate results from get_results_from_emas...")
    processed_results = get_results_from_emas(result)
    print("Results processed by get_results_from_emas retrieved successfully.")

    print("Validating processed results for '200 level Rain'...")
    
    assert "necessary checks" in processed_results
    assert "personal checks" in processed_results
    assert "semester performance" in processed_results
    print("Processed results structure validated successfully.")

    assert processed_results["semester performance"]["status"] == "convergence"
    assert processed_results["semester performance"]["type"] == "flattening"
    
    print("Processed results for '200 level Rain' validated successfully.")
    print("All tests for extract_emas and get_results_from_emas passed successfully.")

@pytest.fixture
def correlation_details():
    return {
        ('total_units', 'gpa'): {'value': -0.46, 'type': 'Negative', 'strength': 'Moderate'},
        ('total_units', 'cgpa'): {'value': 0.11, 'type': 'Positive', 'strength': 'Very Weak'},
        ('gpa', 'cgpa'): {'value': 0.73, 'type': 'Positive', 'strength': 'Strong'},
        ('gpa', 'semester_course_count'): {'value': -0.41, 'type': 'Negative', 'strength': 'Moderate'},
        ('cgpa', 'semester_course_count'): {'value': 0.15, 'type': 'Positive', 'strength': 'Very Weak'}
    }

@pytest.fixture
def partial_corr():
    return {
        ('Accessories', 'gpa'): {'partial_corr': 0.933129, 'prob_val': 0.020549, 'significance': 'Very significant', 'strength': 'Very Strong', 'type': 'Positive'},
        ('Accessories', 'cgpa'): {'partial_corr': 0.960561, 'prob_val': 0.009346, 'significance': 'Very significant', 'strength': 'Very Strong', 'type': 'Positive'},
        ('Accessories_units', 'gpa'): {'partial_corr': -0.241435, 'prob_val': 0.695608, 'significance': 'Insignificant', 'strength': 'Weak', 'type': 'Negative'},
        ('Accessories_units', 'cgpa'): {'partial_corr': 0.10403, 'prob_val': 0.867784, 'significance': 'Insignificant', 'strength': 'Very Weak', 'type': 'Positive'},
        ('Accessories_count', 'gpa'): {'partial_corr': 0.242804, 'prob_val': 0.693918, 'significance': 'Insignificant', 'strength': 'Weak', 'type': 'Positive'},
        ('Accessories_count', 'cgpa'): {'partial_corr': 0.677484, 'prob_val': 0.208904, 'significance': 'Insignificant', 'strength': 'Strong', 'type': 'Positive'},
        ('semester_course_count', 'gpa'): {'partial_corr': 0.146721, 'prob_val': 0.753591, 'significance': 'Insignificant', 'strength': 'Very Weak', 'type': 'Positive'},
        ('semester_course_count', 'cgpa'): {'partial_corr': 0.136078, 'prob_val': 0.77112, 'significance': 'Insignificant', 'strength': 'Very Weak', 'type': 'Positive'},
        ('Mathematics For Economists', 'gpa'): {'partial_corr': 0.265681, 'prob_val': 0.665747, 'significance': 'Insignificant', 'strength': 'Weak', 'type': 'Positive'},
        ('Mathematics For Economists', 'cgpa'): {'partial_corr': 0.817241, 'prob_val': 0.091175, 'significance': 'Significant', 'strength': 'Very Strong', 'type': 'Positive'},
        ('Mathematics For Economists_units', 'gpa'): {'partial_corr': -0.706252, 'prob_val': 0.18246, 'significance': 'Insignificant', 'strength': 'Strong', 'type': 'Negative'},
        ('Mathematics For Economists_units', 'cgpa'): {'partial_corr': 0.543636, 'prob_val': 0.343615, 'significance': 'Insignificant', 'strength': 'Moderate', 'type': 'Positive'},
        ('Mathematics For Economists_count', 'gpa'): {'partial_corr': -0.706252, 'prob_val': 0.18246, 'significance': 'Insignificant', 'strength': 'Strong', 'type': 'Negative'},
        ('Mathematics For Economists_count', 'cgpa'): {'partial_corr': 0.543636, 'prob_val': 0.343615, 'significance': 'Insignificant', 'strength': 'Moderate', 'type': 'Positive'},
        ('Microeconomics', 'gpa'): {'partial_corr': 0.340521, 'prob_val': 0.574966, 'significance': 'Insignificant', 'strength': 'Weak', 'type': 'Positive'},
        ('Microeconomics', 'cgpa'): {'partial_corr': -0.860843, 'prob_val': 0.060998, 'significance': 'Significant', 'strength': 'Very Strong', 'type': 'Negative'},
        ('Microeconomics_units', 'gpa'): {'partial_corr': -0.843364, 'prob_val': 0.072643, 'significance': 'Significant', 'strength': 'Very Strong', 'type': 'Negative'},
        ('Microeconomics_units', 'cgpa'): {'partial_corr': 0.306945, 'prob_val': 0.615412, 'significance': 'Insignificant', 'strength': 'Weak', 'type': 'Positive'}
    }

@pytest.fixture
def student_emas():
    return {
        'semester performance': {
            'status': 'convergence', 'type': 'flattening'
        },

        'necessary checks': {
            'gpa_and_cgpa_ema': (True, 'positive'), 
            'gpa_and_cgpa_emas': (False, 'no crossover'), 
            'gpa_and_gpa_ema': (True, 'positive')
        }, 

        'personal checks': {
            'cgpa_ema_and_Accessories': (True, 'positive'), 
            'gpa_ema_and_Accessories': (True, 'positive'), 
            'cgpa_ema_and_Mathematics For Economists': (False, 'no crossover'), 
            'gpa_ema_and_Mathematics For Economists': (False, 'no crossover'), 
            'cgpa_ema_and_Microeconomics': (False, 'no crossover'), 
            'gpa_ema_and_Microeconomics': (False, 'no crossover'), 
            'cgpa_ema_and_Macroeconomics': (True, 'positive'), 
            'gpa_ema_and_Macroeconomics': (True, 'positive')
        }
    }

def test_extracted_needed_data(correlation_details, partial_corr, student_emas):
    result = extract_needed_data(correlation_details, partial_corr, student_emas)
    
    filtered_corr_data = result['filtered_corr_data']
    assert isinstance(filtered_corr_data, list)
    assert len(filtered_corr_data) == 3
    for item in filtered_corr_data:
        assert 'key' in item
        assert 'strength' in item
        assert item['strength'] in ["Moderate", "Strong", "Very Strong"]
    
    filtered_par_corr_data = result['filtered_par_corr_data']
    assert isinstance(filtered_par_corr_data, list)
    assert len(filtered_par_corr_data) > 0
    for item in filtered_par_corr_data:
        assert 'key' in item
        assert 'significance' in item
        assert 'strength' in item
        assert 'type' in item
        assert item['significance'] in ["Significant", "Very significant"]
        assert item['strength'] in ["Moderate", "Strong", "Very Strong"]

    filtered_emas_data = result['filtered_emas_data']
    assert isinstance(filtered_emas_data, dict)
    
    assert "semester performance" in filtered_emas_data
    assert filtered_emas_data["semester performance"] == student_emas["semester performance"]
    
    assert "necessary checks" in filtered_emas_data
    necessary_checks = filtered_emas_data["necessary checks"]
    assert isinstance(necessary_checks, dict)
    for key, value in necessary_checks.items():
        assert key in student_emas["necessary checks"]
        assert value["crossover"] == student_emas["necessary checks"][key][0]
        assert value["cross_type"] == student_emas["necessary checks"][key][1]
    
    assert "personal checks" in filtered_emas_data
    personal_checks = filtered_emas_data["personal checks"]
    assert isinstance(personal_checks, dict)
    for key, value in personal_checks.items():
        assert key in student_emas["personal checks"]
        assert value["crossover"] == student_emas["personal checks"][key][0]
        assert value["cross_type"] == student_emas["personal checks"][key][1]
