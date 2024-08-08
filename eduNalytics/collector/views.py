from django.shortcuts import render, redirect
import asyncio
from .scrape import run_scrape_script

def scrape(request):
    if request.method == "POST":
        matric_number = request.POST.get("matric_number")
        password = request.POST.get("password")
        
        # Run the scrape function
        scrape_result = asyncio.run(run_scrape_script(matric_number, password))

        # Prepare the data for the table
        course_details = []
        for course in scrape_result['CourseResults']:
            course_details.append({
                'session': course.get('Session', 'unavailable'),
                'semester': course.get('Semester', 'unavailable'),
                'course_code': course.get('Course', 'unavailable'),
                'branch': 'unavailable',  # Branch not yet registered in the database
                'grade': course.get('Grade', 'unavailable'),
                'unit': 'unavailable'  # Units not yet registered in the database
            })

        context = {
            'course_details': course_details,
            'student_info': scrape_result['StudentInfo'],
        }

        # Render the results in a new HTML page
        return render(request, 'collector/assessment.html', context)

    return redirect('home:home')
