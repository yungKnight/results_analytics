import pytest
from collections import defaultdict
from collector.models import Student, Department
from analyzer.models import DetailedCourseResult
from analyzer.utils import filter_results_by_level_semester

@pytest.mark.django_db
def test_filter_results_by_level_semester_with_foreign_key():
    department = Department.objects.create(name='Science')

    student = Student.objects.create(
        name='John Doe', entry_type='UTME', department=department
    )

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

    DetailedCourseResult.objects.create(
        student=student, course='MTH201', branch='Science', grade='B', unit=3,
        score=78, level='200', semester='Harmattan'
    )
    DetailedCourseResult.objects.create(
        student=student, course='PHY201', branch='Science', grade='A', unit=3,
        score=85, level='200', semester='Rain'
    )

    grouped_results = filter_results_by_level_semester(student)

    assert isinstance(grouped_results, defaultdict)

    assert len(grouped_results) == 4

    harmattan_100_results = grouped_results['100 level Harmattan']
    assert len(harmattan_100_results) == 2 
    assert harmattan_100_results[0]['course'] == 'MTH101'
    assert harmattan_100_results[1]['course'] == 'PHY101'

    rain_100_results = grouped_results['100 level Rain']
    assert len(rain_100_results) == 1 
    assert rain_100_results[0]['course'] == 'ENG101'

    harmattan_200_results = grouped_results['200 level Harmattan']
    assert len(harmattan_200_results) == 1 
    assert harmattan_200_results[0]['course'] == 'MTH201'

    rain_200_results = grouped_results['200 level Rain']
    assert len(rain_200_results) == 1
    assert rain_200_results[0]['course'] == 'PHY201'
