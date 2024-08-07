from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'index.html'

    def post(self, request):
        matric_number = request.POST.get('matric_number')
        password = request.POST.get('password')
        context = {'matric_number': matric_number, 'password': password}
        return render(request, 'home/index.html', context)
