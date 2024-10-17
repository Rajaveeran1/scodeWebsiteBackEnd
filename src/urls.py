from django.urls import path
from .views import *

urlpatterns = [
    path('internships/', InternshipList.as_view(), name='internship-list'),
    path('services/', ServiceList.as_view(), name='services-list'),
    path('active-projects/', ActiveProjectList.as_view(), name='active-project-list'),
    path('products/', ProductList.as_view(), name='products-list'),
    path('jobs/', JobsList.as_view(), name='jobs-list'),
]
