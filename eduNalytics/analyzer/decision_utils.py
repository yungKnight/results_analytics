import json

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

def extract_partial_corr(par_corr):
	par_correlation_list = json.loads(par_corr)

	extracted_partials = {}
	for param in par_correlation_list:
		x = param['x']
		y =param['y']
		n = abs(param['n'])
		r = float(param['r'])
		p_val = float(param['p_val'])

		variable_pair = (x, y)

		extracted_partials[variable_pair] = {
			'partial_corr': r,
			'prob_val': p_val,
			'observations': n
		}
	return extracted_partials

def get_partial_corr_result(r, p_val):
    r = float(r)
    p_val = float(p_val)

    correlation_type = "Positive" if r > 0 else "Negative" if r < 0 else "No Correlation"
    
    if p_val < 0.05:
        significance = "Very significant"
    elif p_val < 0.10:
        significance = "Significant"
    else:
        significance = "Insignificant"

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

    return significance, strength, correlation_type

def extract_emas(emas):
    emas_list = json.loads(emas)

    extracted_exponentials = {}
    for param in emas_list:
        semester = param['semester']
        gpa = param['gpa']
        cgpa = param['cgpa']
        gpa_ema = param['gpa_ema']
        cgpa_ema = param['cgpa_ema']

        extracted_exponentials[semester] = {
            "gpa": gpa,
            "cgpa": cgpa,
            "gpa_ema": gpa_ema,
            "cgpa_ema": cgpa_ema,
            "user_specific_params": {}
        }

        for key, value in param.items():
            if key not in ["semester", "gpa", "cgpa", "gpa_ema", "cgpa_ema"]:
                extracted_exponentials[semester]["user_specific_params"][key] = value

    return extracted_exponentials            

#from my extracted emas using extract_emas()
#I'm to check for this conditions
# 1. It should check for divergence/convergence
# 2. It would also check if 1 is a positive scenario or not
# 3. It should also check for crossovers of both ema params

def get_results_from_emas(context_exponentials, semesters):
    """
    Analyze the context_exponentials and semesters to dynamically create inner functions
    for divergence, convergence, or new student observations.
    """
    print("\nAnalyzing context_exponentials...\n")
    print(context_exponentials)

    if len(semesters) > 1:
        print("\nMore than one semester detected. Creating analysis functions...\n")
        last_two_semesters = semesters[-2:]

        prev_semester = last_two_semesters[0]
        current_semester = last_two_semesters[1]
        print(f"this- {prev_semester} is my previous semester, current semester is {current_semester}")

        prev_semester_cgpa_ema = context_exponentials[prev_semester]["cgpa_ema"]
        prev_semester_gpa_ema = context_exponentials[prev_semester]["gpa_ema"]
        prev_semester_cgpa = context_exponentials[prev_semester]["cgpa"]
        prev_semester_gpa = context_exponentials[prev_semester]["gpa"]
        
        current_semester_cgpa_ema = context_exponentials[current_semester]["cgpa_ema"]
        current_semester_gpa_ema = context_exponentials[current_semester]["gpa_ema"]
        current_semester_cgpa = context_exponentials[current_semester]["cgpa"]
        current_semester_gpa = context_exponentials[current_semester]["gpa"]

        print(f"\n My previous semester's gpa ema is {prev_semester_gpa_ema} and current one is {current_semester_gpa_ema}")
        print(f"\n My previous semester's cgpa ema is {prev_semester_cgpa_ema} and current one is {current_semester_cgpa_ema}")
        print(f"\n My previous semester's gpa is {prev_semester_gpa} and current one is {current_semester_gpa}")
        print(f"\n My previous semester's cgpa is {prev_semester_cgpa} and current one is {current_semester_cgpa}")

        def divergence_or_convergence_checker():
            status = "At equilibrium state"
            if ((current_semester_cgpa_ema - current_semester_gpa_ema) > (prev_semester_cgpa_ema - prev_semester_gpa_ema)):
                status = "divergence"
            elif ((current_semester_cgpa_ema - current_semester_gpa_ema) < (prev_semester_cgpa_ema - prev_semester_gpa_ema)):
                status = "convergence"

            return status

        status = divergence_or_convergence_checker()
        print("\nDivergence/Convergence status:", status)

        if ((status == "divergence") & (current_semester_gpa_ema > current_semester_cgpa_ema)):
            type = "positive"
        elif ((status == "divergence") & (current_semester_gpa_ema < current_semester_cgpa_ema)):
            type = "negative"
        elif ((status == "convergence") & ((current_semester_gpa_ema > prev_semester_gpa_ema) & (current_semester_cgpa_ema > prev_semester_cgpa_ema))):
            type = "positive"
        elif ((status == "convergence") & ((current_semester_gpa_ema < prev_semester_gpa_ema) & (current_semester_cgpa_ema < prev_semester_cgpa_ema))):
            type = "negative"
        elif ((status == "convergence") & ((current_semester_gpa_ema > prev_semester_gpa_ema) & (current_semester_cgpa_ema < prev_semester_cgpa_ema))):
            type = "flattening"

        print(f"\nThis is a {type} {status}\n")

        def check_ema_crossover(current_semester_cgpa_ema, prev_semester_gpa, current_semester_gpa):
            step = 0.01
            
            gpa_range = [round(prev_semester_gpa + step * value, 2) 
                         for value in range(int((current_semester_gpa - prev_semester_gpa) / step) + 1)]
            crossover = current_semester_cgpa_ema in gpa_range
            return gpa_range, crossover

        gpa_range, crossover = check_ema_crossover(current_semester_cgpa_ema, prev_semester_gpa, current_semester_gpa)
        print(f"\n My gpa range is {gpa_range} and Did a crossover happen? {crossover}")
    else:
        print("\nOnly one semester detected. Creating observation function...\n")
