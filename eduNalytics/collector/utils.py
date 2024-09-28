from django.core.exceptions import ValidationError
import re

# Program lengths based on departments
program_lengths = {
    'Economics': 5,   # Economics is a 5-year program
    'Medicine': 7,    # Medicine is a 7-year program
    'Engineering': 5, # Engineering is a 5-year program
    # Add more departments and their lengths as needed
}

# Dictionary to track repetition counts for each course code
repetition_count_map = {}

def get_program_length_by_department(department):
    """
    Fetch the program length from the mapping, defaulting to 4 years if unknown.
    """
    return program_lengths.get(department, 4)

def get_semester(course_code):
    """
    Determine the semester (Rain or Harmattan) based on the last digit of the course code.
    """
    try:
        last_digit = int(course_code[-1])
        if last_digit % 2 == 0:
            return 'Rain'
        return 'Harmattan'
    except ValueError:
        raise ValidationError(f"Invalid course code: {course_code}")

def get_level(course_code, department):
    """
    Determine the academic level based on the course code and department.
    Handles repetition counts and extra years if the course is repeated.
    """
    # Extract the first integer from the course code (e.g., 101, 504)
    first_integer_match = re.search(r'\d+', course_code)

    if first_integer_match:
        first_integer = int(first_integer_match.group())

        # Determine the program length dynamically based on the department
        program_length = get_program_length_by_department(department)
        final_level = program_length * 100  # E.g., 5-year program -> 500 level

        # Sanitize the course code by replacing spaces with underscores
        sanitized_course_code = course_code.replace(" ", "_")

        # Get the current repetition count, defaulting to 0
        repetition_count = repetition_count_map.get(sanitized_course_code, 0)

        # Adjust the level based on the repetition count
        if repetition_count == 0:
            # If no repetitions, determine the level normally
            adjusted_level = first_integer
        else:
            # Repetition count starts only after the first completion
            adjusted_level = first_integer + (repetition_count * 100)

        # Update the repetition count in the dictionary
        repetition_count_map[sanitized_course_code] = repetition_count + 1

        # Determine the level based on the adjusted level and the program length
        if adjusted_level < 100:
            return 'Invalid course code'

        if adjusted_level >= 100 and adjusted_level < 200:
            return '100 level'
        elif adjusted_level >= 200 and adjusted_level < 300:
            return '200 level'
        elif adjusted_level >= 300 and adjusted_level < 400:
            return '300 level'
        elif adjusted_level >= 400 and adjusted_level < 500:
            return '400 level'
        elif adjusted_level >= 500 and adjusted_level < 600:
            if program_length >= 5:
                return '500 level' if repetition_count == 0 else 'Extra year (repeating courses)'
        elif adjusted_level >= 600 and adjusted_level < 700:
            if program_length >= 6:
                return '600 level' if repetition_count == 0 else 'Extra year (repeating courses)'
        elif adjusted_level >= 700 and adjusted_level < 800:
            if program_length >= 7:
                return '700 level' if repetition_count == 0 else 'Extra year (repeating courses)'

        # After completing the program's final level, any further repetitions are "Extra year"
        if adjusted_level >= final_level:
            return 'Extra year (repeating courses)'

        return 'Unknown level'
    else:
        return 'Invalid course code format'
