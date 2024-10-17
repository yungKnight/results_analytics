import pytest
from django.db.utils import IntegrityError
from analyzer.results_utils import calculate_cgpa, cleaned_results_by_semester
from analyzer.models import DetailedCourseResult
from collector.models import Student, Department


@pytest.mark.django_db
def test_calculate_cgpa_and_semester_sorting():
    department = Department.objects.create(name="Computer Science")
    student = Student.objects.create(name="John Doe", entry_type="UTME", department=department)
    
    # Add mock DetailedCourseResult data for different semesters and levels
    DetailedCourseResult.objects.create(
        student=student, level="100", semester="Harmattan", course="CSC101", unit=3, branch="General", grade="A", score=85
    )
    DetailedCourseResult.objects.create(
        student=student, level="100", semester="Rain", course="CSC102", unit=3, branch="General", grade="B", score=75
    )
    DetailedCourseResult.objects.create(
        student=student, level="200", semester="Harmattan", course="CSC201", unit=3, branch="General", grade="C", score=65
    )
    DetailedCourseResult.objects.create(
        student=student, level="200", semester="Rain", course="CSC202", unit=3, branch="General", grade="B", score=70
    )

    cgpa_data = calculate_cgpa(student)

    sorted_semesters = list(cgpa_data.keys())
    expected_semesters = [
        "100 level Harmattan",
        "100 level Rain",
        "200 level Harmattan",
        "200 level Rain"
    ]

    assert sorted_semesters == expected_semesters, f"Semesters are not sorted correctly: {sorted_semesters}"

    # Test 2: Check if CGPA is calculated correctly after each semester
    # GPA Calculation:
    # 100 level Harmattan -> GPA: A(5) * 3 = 15 points / 3 units = 5.0
    # 100 level Rain -> GPA: B(4) * 3 = 12 points / 3 units = 4.0
    # CGPA after 100 level = (15 + 12) points / (3 + 3) units = 4.5
    # 200 level Harmattan -> GPA: C(3) * 3 = 9 points / 3 units = 3.0
    # CGPA after 200 level Harmattan = (15 + 12 + 9) points / (3 + 3 + 3) units = 4.0
    # 200 level Rain -> GPA: B(4) * 3 = 12 points / 3 units = 4.0
    # Final CGPA after 200 level Rain = (15 + 12 + 9 + 12) points / (3 + 3 + 3 + 3) units = 4.0

    print('confirming the CGPA calculation is correct')
    assert cgpa_data["100 level Harmattan"]['CGPA'] == 5.0
    assert cgpa_data["100 level Rain"]['CGPA'] == 4.5
    assert cgpa_data["200 level Harmattan"]['CGPA'] == 4.0
    assert cgpa_data["200 level Rain"]['CGPA'] == 4.0
    print('confirmed')



