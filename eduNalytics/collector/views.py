from django.shortcuts import render, redirect
import asyncio
from .scrape import run_scrape_script
from .models import Course, CourseOffering, Student, Department
from datetime import timedelta
from .utils import get_level
from analyzer.utils import process_detailed_course_results, filter_results_by_level_semester
import re
from collections import defaultdict

def scrape(request):
    if request.method == "POST":
        matric_number = request.POST.get("matric_number")
        password = request.POST.get("password")

        try:
            scrape_result = asyncio.run(run_scrape_script(matric_number, password))
        except Exception as e:
            request.session['error_message'] = str(e)
            return redirect('home:home')

        if 'error' in scrape_result:
            request.session['error_message'] = scrape_result.get('error', 'Unknown error occurred')
            return redirect('home:home')

        student_info = scrape_result['StudentInfo']
        name = student_info['Name']
        department_name = student_info['Department']
        entry_type = 'UTME' if student_info['EntryType'].lower() == 'utme' else 'Diploma'

        department, _ = Department.objects.get_or_create(name=department_name)
        student, _ = Student.objects.get_or_create(
            name=name,
            entry_type=entry_type,
            department=department
        )

        # Initialize a dictionary to group course details by semester and level
        grouped_course_details = defaultdict(list)

        for course in scrape_result['CourseResults']:
            course_code = course.get('Course', 'unavailable')
            course_obj = Course.objects.filter(code=course_code).first()

            session = course.get('Session', 'unavailable')
            semester = course.get('Semester', 'unavailable')
            level = course.get('Level', 'unavailable')
            grade = course.get('Grade', 'unavailable')
            score = course.get('Score', 0)

            if course_obj:
                course_offering = CourseOffering.objects.filter(course=course_obj, department=department).first()

                if not course_offering:
                    level = get_level(course_code, department)
                    grouped_course_details[(session, semester, level)].append({
                        'course_code': course_code,
                        'branch': 'unavailable',
                        'grade': grade,
                        'unit': 'unavailable',
                        'score': score
                    })
                    continue

                grouped_course_details[(session, semester, level)].append({
                    'course_code': course_code,
                    'branch': course_offering.branch.name,
                    'grade': grade,
                    'unit': course_offering.units,
                    'score': score
                })
            else:
                # Handle non-course object instances
                level_string = course.get('Level', 'unavailable')
                if re.search(r'\d+', level_string):  # Handle numerical levels
                    level = re.search(r'\d+', level_string).group(0)
                else:
                    level = 'extra year'  # Default to 'extra year' for non-numerical levels

                grouped_course_details[(session, semester, level)].append({
                    'course_code': course_code,
                    'branch': 'unavailable',
                    'grade': grade,
                    'unit': 'unavailable',
                    'score': score
                })

        # Flatten the grouped course details into a list for rendering
        course_details = []
        for (session, semester, level), courses in grouped_course_details.items():
            for course in courses:
                course.update({
                    'session': session,
                    'semester': semester,
                    'level': level
                })
                course_details.append(course)

        process_detailed_course_results(student_info, course_details)

        request.session['context'] = {
            'course_details': course_details,
            'student_info': student_info,
        }
        request.session.set_expiry(timedelta(minutes=15))

        return redirect('analyzer:cleaned_results')

    return redirect('home:welcome')
