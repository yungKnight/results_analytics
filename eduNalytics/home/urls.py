from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.WelcomeView.as_view(), name='welcome'),
    path('Details', views.HomeView.as_view(), name='home'),
]
