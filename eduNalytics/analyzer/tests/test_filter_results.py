import pytest
from collections import defaultdict
from collector.models import Student, Department
from analyzer.models import DetailedCourseResult
from analyzer.utils import filter_results_by_level_semester

@pytest.mark.django_db
def test_filter_results_by_level_semester_with_foreign_key():
    # Create a test department
    department = Department.objects.create(name='Science')

    # Create a test student
    student = Student.objects.create(
        name='John Doe', entry_type='UTME', department=department
    )

    # Create mock DetailedCourseResult instances for 100 level
    DetailedCourseResult.objects.create(
        student=student, course='MTH101', branch='Science', grade='A', unit=3,
        score=85, level='100', semester='Harmattan'
    )
    DetailedCourseResult.objects.create(
        student=student, course='PHY101', branch='Science', grade='B', unit=3,
        score=75, level='100', semester='Harmattan'
    )
    DetailedCourseResult.objects.create(
        student=student, course='ENG101', branch='Arts', grade='A', unit=2,
        score=88, level='100', semester='Rain'
    )

    # Create mock DetailedCourseResult instances for 200 level
    DetailedCourseResult.objects.create(
        student=student, course='MTH201', branch='Science', grade='B', unit=3,
        score=78, level='200', semester='Harmattan'
    )
    DetailedCourseResult.objects.create(
        student=student, course='PHY201', branch='Science', grade='A', unit=3,
        score=85, level='200', semester='Rain'
    )

    # Call the function to test
    grouped_results = filter_results_by_level_semester(student)

    # Check that the function returns a dictionary
    assert isinstance(grouped_results, defaultdict)

    # Check that the results are grouped correctly by level and semester
    assert len(grouped_results) == 4  # Four distinct groups: 100 Harmattan, 100 Rain, 200 Harmattan, 200 Rain

    # Check contents of the '100 level Harmattan' group
    harmattan_100_results = grouped_results['100 level Harmattan']
    assert len(harmattan_100_results) == 2  # Two courses for 100 level Harmattan
    assert harmattan_100_results[0]['course'] == 'MTH101'
    assert harmattan_100_results[1]['course'] == 'PHY101'

    # Check contents of the '100 level Rain' group
    rain_100_results = grouped_results['100 level Rain']
    assert len(rain_100_results) == 1  # One course for 100 level Rain
    assert rain_100_results[0]['course'] == 'ENG101'

    # Check contents of the '200 level Harmattan' group
    harmattan_200_results = grouped_results['200 level Harmattan']
    assert len(harmattan_200_results) == 1  # One course for 200 level Harmattan
    assert harmattan_200_results[0]['course'] == 'MTH201'

    # Check contents of the '200 level Rain' group
    rain_200_results = grouped_results['200 level Rain']
    assert len(rain_200_results) == 1  # One course for 200 level Rain
    assert rain_200_results[0]['course'] == 'PHY201'
