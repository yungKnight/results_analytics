import pytest
from django.core.exceptions import ValidationError
from collector.utils import get_semester

@pytest.mark.parametrize("course_code, expected_semester, expect_error", [
    ('ECO101', 'Harmattan', False),
    ('ENG102', 'Rain', False),
    ('MED201', 'Harmattan', False),
    ('XXX', None, True),  # Invalid course code that raises an error
])

def test_get_semester(course_code, expected_semester, expect_error):
    if expect_error:
        with pytest.raises(ValidationError) as excinfo:
            get_semester(course_code)
        print(f"Error raised for course_code: {course_code}, Error: {excinfo.value}")
    else:
        result = get_semester(course_code)
        print(f"Testing course_code: {course_code}, Result: {result}")
        assert result == expected_semester