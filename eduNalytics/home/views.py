from django.shortcuts import render, redirect
from django.views.generic import TemplateView

class WelcomeView(TemplateView):
    template_name = 'welcome.html'

    def post(self, request):
        username = request.POST.get('username')
        if username:
            request.session['username'] = username
            return redirect('home:home')
        return render(request, self.template_name)


class HomeView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if 'username' not in request.session:
            return redirect('home:welcome')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.get('username', '')
        context['error_message'] = self.request.session.pop('error_message', None)
        return context
