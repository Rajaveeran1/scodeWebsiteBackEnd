from django.urls import path
from .views import *

urlpatterns = [
    path('internships/', InternshipList.as_view(), name='internship-list'),
    path('services/', ServiceList.as_view(), name='services-list'),
    path('projects/', ProjectList.as_view(), name='project-list'),
]
