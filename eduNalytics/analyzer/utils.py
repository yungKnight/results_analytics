from .models import DetailedCourseResult 
from collector.models import Student

def process_detailed_course_results(student_info, course_details):
    student_name = student_info['Name']
    entry_type = 'UTME' if student_info['EntryType'].lower() == 'utme' else 'Diploma'

    student = Student.objects.filter(name=student_name, entry_type=entry_type).first()

    if student:
        for course in course_details:
            unit = course['unit'] if course['unit'] != 'unavailable' else 2
            try:
                unit = int(unit)
            except ValueError:
                unit = 2 

            existing_result = DetailedCourseResult.objects.filter(
                student=student,
                course=course['course_code'],
                level=course['level'],
                semester=course['semester']
            ).first()

            if not existing_result:
                DetailedCourseResult.objects.create(
                    student=student,
                    semester=course['semester'],
                    level=course['level'],
                    course=course['course_code'],
                    branch=course['branch'],
                    grade=course['grade'],
                    unit=unit,
                    score=course['score']
                )
            else:
                existing_result.unit = unit
                existing_result.branch = course['branch']
                existing_result.save()

