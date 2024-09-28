import asyncio
import os
import re
import json
from scrapy.http import HtmlResponse
from playwright.async_api import async_playwright
from .utils import get_semester, get_level

async def run_scrape_script(matric, pword):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            context = await browser.new_context()
            page = await context.new_page()

            async def handle_request(route, request):
                if request.resource_type == 'image':
                    await route.abort()
                else:
                    await route.continue_()

            await page.route("**/*", handle_request)

            url = 'https://stdportal.oouagoiwoye.edu.ng/index.php'
            await page.goto(url, timeout=0)

            await page.fill("input#jamb", matric)
            await page.fill("input#sname", pword)
            await page.click('button.btn')

            await page.goto('https://stdportal.oouagoiwoye.edu.ng/dashboard.php')

            tbodies = await page.query_selector_all('tbody')
            if len(tbodies) < 2:
                raise ValueError("Less than 2 tbody elements found on the page")

            personal = await page.query_selector_all('h4 span strong')
            name_element = personal[0]
            status_element = personal[1]

            name = await name_element.inner_text()
            status = await status_element.inner_text()
            
            pattern = re.compile(r'^([A-Z]+),\s*([A-Z])[a-z]*(?:\s+([A-Z]))?[a-z]*')
            match = re.match(pattern, name)
            formatted_name = f"{match.group(1)} {match.group(2)}.{match.group(3) or ''}"

            second_tbody = tbodies[1]
            table_rows = await second_tbody.query_selector_all('tr')

            entry_type_row = table_rows[5]
            department_row = table_rows[10]

            type_of_entry = await (await entry_type_row.query_selector_all('td'))[1].inner_text()
            department = await (await department_row.query_selector_all('td'))[2].inner_text()

            await page.wait_for_selector('div.modal-content')
            await (await page.query_selector('div.modal-header span.close')).click()

            await (await page.query_selector('a[href="results.php"]')).click()

            await page.wait_for_selector('div.col-xs-12.col-sm-6')

            html_content = await page.content()
            response = HtmlResponse(url=page.url, body=html_content.encode(), encoding='utf-8')
            results = response.css('div.form-group')[1:-2]

            your_result = []
            for result in results:
                course_code = result.css('div.col-sm-1::text').get().strip()
                try:
                    semester = get_semester(course_code)
                except ValidationError:
                    semester = 'Unknown'

                try:
                    level = get_level(course_code, department)
                except ValidationError:
                    level = 'Unknown'

                your_result.append({
                    'Session': result.css('div.col-sm-2::text').get().strip(),
                    'Course': course_code,
                    'Grade': result.css('div.col-sm-1:nth-child(6)::text').get().strip(),
                    'Score': result.css('div.col-sm-2:nth-child(4)::text').get().strip(),
                    'Semester': semester, 
                    'Level': level
                })

            student_info = {
                'Name': formatted_name,
                'Status': status.capitalize(),
                'Department': department,
                'EntryType': type_of_entry.capitalize()
            }

            result_data = {
                'StudentInfo': student_info,
                'CourseResults': your_result
            }

            await browser.close()
            return result_data
        
    except ValueError:
        return {'error': 'Wrong credentials. Try again'}
    except Exception:
        return {'error': 'Error connecting...program unable to access servers'}