from django.urls import path
from . import views

app_name = 'collector'

urlpatterns = [
    path('scrape/', views.scrape, name='scrape'),
    path('scrape/results/', views.results, name='results'),
]