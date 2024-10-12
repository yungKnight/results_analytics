import pytest
from collector.models import Student, Department
from analyzer.models import DetailedCourseResult
from analyzer.results_utils import calculate_cgpa

@pytest.mark.django_db
def test_calculate_cgpa_no_courses():
    # Set up department and student
    department = Department.objects.create(name="Economics")
    student = Student.objects.create(name="Jane Doe", entry_type="UTME", department=department)

    # Calculate CGPA with no courses
    semester_cgpas = calculate_cgpa(student)

    # Verify that the result is empty or contains zero CGPA
    assert semester_cgpas == [], "Expected no CGPA values when no courses are present."
    print('No CGPA values expected here')

def test_calculate_cgpa_with_courses():
    department = Department.objects.create(name="Economics")
    student = Student.objects.create(name="John Doe", entry_type="UTME", department=department)

    courses_data = [
        {"grade": "A", "unit": 3, "level": "100", "semester": "Harmattan", "course": "ECON101"},
        {"grade": "B", "unit": 4, "level": "100", "semester": "Harmattan", "course": "ECON102"},
        {"grade": "A", "unit": 2, "level": "100", "semester": "Rain", "course": "ECON103"},
        {"grade": "C", "unit": 3, "level": "100", "semester": "Rain", "course": "ECON104"},
        {"grade": "B", "unit": 3, "level": "200", "semester": "Harmattan", "course": "ECON201"},
        {"grade": "A", "unit": 3, "level": "200", "semester": "Harmattan", "course": "ECON202"},
        {"grade": "D", "unit": 4, "level": "200", "semester": "Rain", "course": "ECON203"},
        {"grade": "C", "unit": 2, "level": "200", "semester": "Rain", "course": "ECON204"},
    ]
    
    for course in courses_data:
        DetailedCourseResult.objects.create(
            student=student,
            course=course["course"],
            branch="Main",
            grade=course["grade"],
            unit=course["unit"],
            level=course["level"],
            semester=course["semester"],
            score=0
        )
        print(f"Created course result for {course['course']}: Grade {course['grade']}, Unit {course['unit']}")

    semester_cgpas = calculate_cgpa(student)
    print(f"Calculated semester CGPAs: {semester_cgpas}")

    total_points = (
        (5 * 3) + (4 * 4) + (5 * 2) + (3 * 3) +  
        (4 * 3) + (5 * 3) + (2 * 4) + (3 * 2)   
    )
    total_units = 3 + 4 + 2 + 3 + 3 + 3 + 4 + 2
    expected_cgpa = total_points / total_units
    print(f"Expected CGPA: {expected_cgpa:.2f} (Total Points: {total_points}, Total Units: {total_units})")

    print(
        f"Comparing calculated CGPA: {round(semester_cgpas[-1], 2)} with expected CGPA: {round(expected_cgpa, 2)}")
    assert round(semester_cgpas[-1], 2) == round(expected_cgpa, 2), f"Expected CGPA: {expected_cgpa}, got: {semester_cgpas[-1]}"
    
    assert len(semester_cgpas) == 4 
    print(f"Test passed. Number of CGPAs calculated: {len(semester_cgpas)}")
