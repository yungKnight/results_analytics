import pytest
from collector.utils import get_level

@pytest.mark.parametrize("course_code, department, repetition_count, expected_level", [
    ('ECO101', 'Economics', 0, '100 level'),
    ('ENG202', 'Engineering', 0, '200 level'),
    ('MED301', 'Medicine', 0, '300 level'),
    ('ECO101', 'Economics', 1, '200 level'),
    ('ECO101', 'Economics', 2, '300 level'),
    ('ECO101', 'Economics', 3, '400 level'),
    ('ECO101', 'Economics', 1, 'Extra year'),
    ('MED401', 'Medicine', 0, '400 level'),
    ('MED501', 'Medicine', 0, '500 level'), 
    ('ECO999', 'Economics', 2, 'Extra year'),
    ('XXX101', 'UnknownDept', 0, 'Invalid course code format'),
    ('MED301', 'Medicine', 0, '300 level'),
    ('ENG500', 'Engineering', 0, '500 level'),
])

def test_get_level(course_code, department, repetition_count, expected_level):
    result = get_level(course_code, department, repetition_count)
    print(f"Testing course_code: {course_code}, department: {department}, repetition_count: {repetition_count}, Result: {result}")
    assert result == expected_level