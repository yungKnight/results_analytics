from django.shortcuts import render, redirect
import asyncio
from .scrape import run_scrape_script
from .models import Course

def scrape(request):
    if request.method == "POST":
        matric_number = request.POST.get("matric_number")
        password = request.POST.get("password")

        try:
            scrape_result = asyncio.run(run_scrape_script(matric_number, password))
        except Exception as e:
            # Handle scrape exceptions (e.g., network issues, invalid credentials)
            request.session['error_message'] = str(e)
            return redirect('home:home')

        if 'error' in scrape_result:
            request.session['error_message'] = scrape_result.get('error', 'Unknown error occurred')
            return redirect('home:home')

        course_details = []
        for course in scrape_result['CourseResults']:
            course_code = course.get('Course', 'unavailable')
            course_obj = Course.objects.filter(code=course_code).first()

            if course_obj:
                branch = course_obj.branch
                units = course_obj.units
            else:
                branch = 'unavailable'
                units = 'unavailable'

            course_details.append({
                'session': course.get('Session', 'unavailable'),
                'semester': course.get('Semester', 'unavailable'),
                'course_code': course_code,
                'branch': branch,
                'grade': course.get('Grade', 'unavailable'),
                'unit': units
            })

        request.session['context'] = {
            'course_details': course_details,
            'student_info': scrape_result['StudentInfo'],
        }

        return redirect('collector:results')

    return redirect('home:home')

def results(request):
    context = request.session.get('context')

    if context:
        del request.session['context']
        return render(request, 'assessment.html', context)

    return redirect('home:home')
