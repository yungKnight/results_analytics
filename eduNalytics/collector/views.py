from django.shortcuts import render, redirect
import asyncio
from .scrape import run_scrape_script
from .models import Course, CourseOffering, CourseResult, Student, Department
from datetime import timedelta

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

        course_details = []
        for course in scrape_result['CourseResults']:
            course_code = course.get('Course', 'unavailable')
            course_obj = Course.objects.filter(code=course_code).first()

            if course_obj:
                course_offering = CourseOffering.objects.filter(course=course_obj, department=department).first()
                if not course_offering:
                    course_details.append({
                        'session': course.get('Session', 'unavailable'),
                        'semester': course.get('Semester', 'unavailable'),
                        'course_code': course_code,
                        'branch': 'unavailable',
                        'grade': course.get('Grade', 'unavailable'),
                        'unit': 'unavailable'
                    })
                    continue

                session = course.get('Session', 'unavailable')
                semester = course.get('Semester', 'unavailable')
                grade = course.get('Grade', 'unavailable')
                score = course.get('Score', 0)

                CourseResult.objects.update_or_create(
                    student=student,
                    course_offering=course_offering,
                    session=session,
                    semester=semester,
                    defaults={'grade': grade, 'score': score}
                )

                course_details.append({
                    'session': session,
                    'semester': semester,
                    'course_code': course_code,
                    'branch': course_offering.branch.name,
                    'grade': grade,
                    'unit': course_offering.units
                })
            else:
                course_details.append({
                    'session': course.get('Session', 'unavailable'),
                    'semester': course.get('Semester', 'unavailable'),
                    'course_code': course_code,
                    'branch': 'unavailable',
                    'grade': course.get('Grade', 'unavailable'),
                    'unit': 'unavailable'
                })

        request.session['context'] = {
            'course_details': course_details,
            'student_info': student_info,
        }
        request.session.set_expiry(timedelta(minutes=15))

        return redirect('collector:results')

    return redirect('home:home')

def results(request):
    context = request.session.get('context')

    if context:
        return render(request, 'assessment.html', context)

    return redirect('home:home')