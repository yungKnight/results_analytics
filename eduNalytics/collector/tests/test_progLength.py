import pytest
from collector.utils import get_program_length_by_department

@pytest.mark.parametrize("department, expected_length", [
    ('Economics', 4),
    ('Medicine', 7),
    ('Engineering', 5),
    ('UnknownDept', 4),
])
def test_get_program_length_by_department(department, expected_length):
    result = get_program_length_by_department(department)
    print(f"Testing department: {department}, Result: {result}")
    assert result == expected_length