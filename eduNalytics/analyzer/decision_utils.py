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
    if len(semesters) > 1:
        print("\nMore than one semester detected. Creating analysis functions...\n")
        last_two_semesters = semesters[-2:]

        prev_semester = last_two_semesters[0]
        current_semester = last_two_semesters[1]
        print(f"this- {prev_semester} is my previous semester, current semester is {current_semester}")

        prev_semester_data = context_exponentials[prev_semester]
        current_semester_data = context_exponentials[current_semester]

        prev_semester_cgpa_ema = prev_semester_data["cgpa_ema"]
        current_semester_cgpa_ema = current_semester_data["cgpa_ema"]

        prev_semester_gpa_ema = prev_semester_data["gpa_ema"]
        current_semester_gpa_ema = current_semester_data["gpa_ema"]

        prev_semester_gpa = prev_semester_data["gpa"]
        current_semester_gpa = current_semester_data["gpa"]

        prev_semester_cgpa = prev_semester_data["cgpa"]
        current_semester_cgpa = current_semester_data["cgpa"]

        user_specific_params_prev = prev_semester_data["user_specific_params"]
        user_specific_params_current = current_semester_data["user_specific_params"]

        print(context_exponentials)
        print(f"Previous semester: {user_specific_params_prev}")
        print(f"Current semester: {user_specific_params_current}")

        #print(f"\n My previous semester's gpa ema is {prev_semester_gpa_ema} and current one is {current_semester_gpa_ema}")
        #print(f"\n My previous semester's cgpa ema is {prev_semester_cgpa_ema} and current one is {current_semester_cgpa_ema}")
        #print(f"\n My previous semester's gpa is {prev_semester_gpa} and current one is {current_semester_gpa}")
        #print(f"\n My previous semester's cgpa is {prev_semester_cgpa} and current one is {current_semester_cgpa}")

        def divergence_or_convergence_checker():
            status = "At equilibrium state"
            if ((current_semester_cgpa_ema - current_semester_gpa_ema) > (prev_semester_cgpa_ema - prev_semester_gpa_ema)):
                status = "divergence"
            elif ((current_semester_cgpa_ema - current_semester_gpa_ema) < (prev_semester_cgpa_ema - prev_semester_gpa_ema)):
                status = "convergence"

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

            return status, type

        status, type = divergence_or_convergence_checker()
        print("\nDivergence/Convergence status:", status)
        print(f"\nThis is a {type} {status}\n")

        def check_ema_crossover(param1, param2, param3):
            step = 0.01
            
            gpa_range = [round(param2 + step * value, 2) 
                         for value in range(int((param3 - param2) / step) + 1)]
            crossover = param1 in gpa_range

            cross_type = "no crossover"
            if crossover:
                cross_type = "at equilibrium"
                if param3 > param1:
                    cross_type = "positive"
                elif param3 < param1:
                    cross_type = "negative"

            return crossover, cross_type

        crossover, cross_type = check_ema_crossover(current_semester_cgpa_ema, prev_semester_gpa, current_semester_gpa)
        print(f"\nDid a crossover happen between my cgpa and gpa? {crossover}")
        print(f"crossover is {cross_type} in nature\n")

        crossover, cross_type = check_ema_crossover(current_semester_cgpa_ema, prev_semester_gpa_ema, current_semester_gpa_ema)
        print(f"\nDid a crossover happen between my cgpa ema and gpa ema? {crossover}")
        print(f"crossover is {cross_type} in nature\n")

        crossover, cross_type = check_ema_crossover(current_semester_gpa_ema, prev_semester_gpa, current_semester_gpa)
        print(f"\nDid a crossover happen between my gpa ema and gpa? {crossover}")
        print(f"crossover is {cross_type} in nature\n")

        if user_specific_params_prev and user_specific_params_current:
            print("Analyzing user-specific parameters for EMA crossover...\n")
            
            for branch, prev_value in user_specific_params_prev.items():
                if branch in user_specific_params_current:
                    current_value = user_specific_params_current[branch]

                    param1 = prev_semester_cgpa_ema
                    param2 = prev_value
                    param3 = current_value

                    crossover, cross_type = check_ema_crossover(param1, param2, param3)
                    print(f"\nDid a crossover happen between my cgpa ema and {branch}? {crossover}")
                    print(f"crossover is {cross_type} in nature\n")
        else:
            print("\nSkipping EMA crossover analysis as user-specific parameters are empty.\n")

    else:
        print("\nOnly one semester detected. Creating observation function...\n")
