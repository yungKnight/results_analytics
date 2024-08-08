from django.urls import path
from .views import scrape

app_name = 'collector'

urlpatterns = [
    path('scrape/', scrape, name='scrape'),
]
