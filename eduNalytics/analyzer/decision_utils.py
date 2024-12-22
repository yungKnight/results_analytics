import json

def display_parsed_part(par_corr):
	print("\nMy context partial correlations:\n")
	print(par_corr)

def display_parsed_emas(emas):
	print("\nMy context emas:\n")
	print(emas)

def extract_correlations(correlations):
    """
    Extract correlations from the provided JSON structure and return a dictionary 
    with parsed variable pairs and their corresponding correlation values.
    
    Parameters:
        correlations (str): JSON string containing correlation data 
                            in the format {"('var1', 'var2')": "value", ...}.
                            
    Returns:
        dict: A dictionary with variable pairs as tuples and their correlation values as floats.
    """
    correlation_dict = json.loads(correlations)
    
    extracted_correlations = {}
    for key, value in correlation_dict.items():
        variable_pair = eval(key)
        correlation_value = float(value)
        extracted_correlations[variable_pair] = correlation_value
    
    return extracted_correlations

def get_correlation(r):
    """
    Determine the type (Positive, Negative, No Correlation) and 
    strength (Very Weak, Weak, Moderate, Strong, Very Strong) of the correlation.

    Parameters:
        r (float): The correlation coefficient.

    Returns:
        tuple: A tuple containing:
            - type (str): The type of correlation (Positive, Negative, No Correlation).
            - strength (str): The strength of the correlation.
    """
    r = float(r)
    correlation_type = "Positive" if r > 0 else "Negative" if r < 0 else "No Correlation"
    
    abs_r = abs(r)
    if abs_r < 0.2:
        strength = "Very Weak"
    elif abs_r < 0.4:
        strength = "Weak"
    elif abs_r < 0.6:
        strength = "Moderate"
    elif abs_r < 0.8:
        strength = "Strong"
    else:
        strength = "Very Strong"
    
    return correlation_type, strength
