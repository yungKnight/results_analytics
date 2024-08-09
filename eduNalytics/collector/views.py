from django.shortcuts import render, redirect
import asyncio
from .scrape import run_scrape_script

def scrape(request):
    if request.method == "POST":
        matric_number = request.POST.get("matric_number")
        password = request.POST.get("password")

        scrape_result = asyncio.run(run_scrape_script(matric_number, password))

        if 'error' in scrape_result:
            return redirect('home:home')

        course_details = []
        for course in scrape_result['CourseResults']:
            course_details.append({
                'session': course.get('Session', 'unavailable'),
                'semester': course.get('Semester', 'unavailable'),
                'course_code': course.get('Course', 'unavailable'),
                'branch': 'unavailable',
                'grade': course.get('Grade', 'unavailable'),
                'unit': 'unavailable'
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