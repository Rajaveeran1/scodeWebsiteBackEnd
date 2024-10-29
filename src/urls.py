from django.urls import path
from .views import *

urlpatterns = [
    path('internships/', InternshipList.as_view(), name='internship-list'),
    path('services/', ServiceList.as_view(), name='services-list'),
    path('active-projects/', ActiveProjectList.as_view(), name='active-project-list'),
    path('products/', ProductList.as_view(), name='products-list'),
    path('jobs/', JobsList.as_view(), name='jobs-list'),
    path('job-application/', JobApplicationView.as_view(), name='job-application-create'),
    path('blogs/', BlogList.as_view(), name='blogs'),
    path('add-comment/', CommentView.as_view(), name='add_comment'),
    path('comments/<int:blog_post_id>/', CommentList.as_view(), name='comment_list_by_blog'),
    path('posts/<int:blog_post_id>/like/', LikeView.as_view(), name='like_blog_post'),
    path('posts/<int:blog_post_id>/view/', ViewCountView.as_view(), name='view_blog_post'),

    path('register/', UserRegisterView.as_view(), name='user-register'),
    
    path('qa/', QuestionAndAnswerView.as_view(), name='question_and_answer'),
]
