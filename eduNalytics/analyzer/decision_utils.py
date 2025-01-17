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

def get_results_from_emas(context_exponentials):
    """
    Analyze the context_exponentials and semesters to dynamically create inner functions
    that checks for divergence or convergence of a student's present performance compared
    to historical performance and what it indicates. It also includes an inner function that
    checks for crossing of historical bounds and what sort of crossing it is.
    """
    semesters = list(context_exponentials.keys())

    if len(semesters) > 1:
        last_two_semesters = semesters[-2:]

        prev_semester = last_two_semesters[0]
        current_semester = last_two_semesters[1]

        prev_semester_data = context_exponentials[prev_semester]
        current_semester_data = context_exponentials[current_semester]

        prev_semester_cgpa_ema = prev_semester_data["cgpa_ema"]
        prev_semester_gpa_ema = prev_semester_data["gpa_ema"]
        prev_semester_gpa = prev_semester_data["gpa"]
        prev_semester_cgpa = prev_semester_data["cgpa"]
        prev_user_specific_params = prev_semester_data["user_specific_params"]

        current_semester_cgpa_ema = current_semester_data["cgpa_ema"]
        current_semester_gpa_ema = current_semester_data["gpa_ema"]
        current_semester_gpa = current_semester_data["gpa"]
        current_semester_cgpa = current_semester_data["cgpa"]
        current_user_specific_params = current_semester_data["user_specific_params"]

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

            return {"status": status, "type": type}

        semester_performance = divergence_or_convergence_checker()

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

        compulsory_emas_check = {
            "gpa_and_cgpa_ema": check_ema_crossover(current_semester_cgpa_ema, prev_semester_gpa, current_semester_gpa),
            "gpa_and_cgpa_emas": check_ema_crossover(current_semester_cgpa_ema, prev_semester_gpa_ema, current_semester_gpa_ema),
            "gpa_and_gpa_ema": check_ema_crossover(current_semester_gpa_ema, prev_semester_gpa, current_semester_gpa)
        }

        branch_specific_checks = {}
        if prev_user_specific_params and current_user_specific_params:
            for branch, prev_value in prev_user_specific_params.items():
                if branch in current_user_specific_params:
                    current_value = current_user_specific_params[branch]
                    
                    param1 = current_semester_cgpa_ema
                    param2 = prev_value
                    param3 = current_value
                    branch_specific_checks[f"cgpa_ema_and_{branch}"] = check_ema_crossover(param1, param2, param3)
                    
                    param1 = current_semester_gpa_ema
                    param2 = prev_value
                    param3 = current_value
                    branch_specific_checks[f"gpa_ema_and_{branch}"] = check_ema_crossover(param1, param2, param3)

      
        ema_results = {
            "semester performance": semester_performance, 
            "necessary checks": compulsory_emas_check, 
            "personal checks": branch_specific_checks
        }
    
        
        return ema_results
    else:
        ema_results = [{}, {}, {}]
        return ema_results

def extract_needed_data(correlation_details, partial_corr, student_emas):
    needed_data = {}
    selected_corr_data = []
    selected_par_corr_data = []
    selected_ema_data = {}

    def extract_needed_corr_params():
        for key, value in correlation_details.items():
            if value['strength'] in ["Moderate", "Strong", "Very Strong"]:
                selected_corr_data.append({'key': key, 'strength': value['strength']})

        needed_data['filtered_corr_data'] = selected_corr_data

    extract_needed_corr_params()

    if partial_corr != {}:
        def extract_needed_par_corr_params():
            for key, value in partial_corr.items():
                if value['significance'] in ["Significant", "Very significant"]:
                    selected_par_corr_data.append(
                        {
                            'key': key,
                            'significance': value['significance'],
                            'strength': value['strength'],
                            'type': value['type'],
                        }
                    )

            needed_data['filtered_par_corr_data'] = selected_par_corr_data

        extract_needed_par_corr_params()

    def extract_needed_ema_params():
        selected_ema_data["semester performance"] = student_emas.get("semester performance", {})
        selected_ema_data["necessary checks"] = {}
        selected_ema_data["personal checks"] = {}
        
        for category, checks in student_emas.items():
            if category in ["necessary checks", "personal checks"]:
                if checks:
                    destructured_checks = {
                        key: {"crossover": value[0], "cross_type": value[1]}
                        for key, value in checks.items()
                    }
                    selected_ema_data[category] = destructured_checks
        
        needed_data["filtered_emas_data"] = selected_ema_data

    extract_needed_ema_params()

    return needed_data

