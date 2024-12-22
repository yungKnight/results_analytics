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
    # Parse the JSON string into a dictionary
    correlation_dict = json.loads(correlations)
    
    # Process the key-value pairs into a structured format
    extracted_correlations = {}
    for key, value in correlation_dict.items():
        variable_pair = eval(key)
        correlation_value = float(value)
        extracted_correlations[variable_pair] = correlation_value
    
    return extracted_correlations
