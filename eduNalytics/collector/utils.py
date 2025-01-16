from django.core.exceptions import ValidationError
import re

program_lengths = {
    'Medicine': 7,
    'Engineering': 5,
    # Add more departments that don't offer 4-year courses as needed
}

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
        return 'Rain' if last_digit % 2 == 0 else 'Harmattan'
    except ValueError:
        raise ValidationError(f"Invalid course code: {course_code}")

def get_level(course_code, department, repetition_count=0):
    """
    Determine the academic level based on the course code and department.
    Handles repetition counts and extra years if the course is repeated.
    """
    first_integer_match = re.search(r'\d+', course_code)

    if first_integer_match:
        first_integer = int(first_integer_match.group())
        program_length = get_program_length_by_department(department)
        final_level = program_length * 100

        adjusted_level = first_integer + (repetition_count * 100)

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
            if program_length == 5:
                return '500 level' if repetition_count == 0 else 'Extra year'
        elif adjusted_level >= 600 and adjusted_level < 700:
            if program_length == 6:
                return '600 level' if repetition_count == 0 else 'Extra year'
        elif adjusted_level >= 700 and adjusted_level < 800:
            if program_length == 7:
                return '700 level' if repetition_count == 0 else 'Extra year'

        if adjusted_level >= final_level:
            return 'Extra year'

        return 'Unknown level'
    else:
        return 'Invalid course code format'