from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
        
from django.contrib.auth import login

   
class InternshipList(APIView):

    def get(self, request, format=None):
        try:
            internships = Internship.objects.all()
            serializer = InternshipSerializer(internships, many=True)
            return Response({
                'success': True,
                'message': 'Internship retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ServiceList(APIView):

    def get(self, request, format=None):
        try:
            services = Service.objects.all()
            serializer = ServiceSerializer(services, many=True, context={'request': request})
            return Response({
                'success': True,
                'message': 'Services retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        


class ActiveProjectList(APIView):

    def get(self, request, format=None):
        try:
            products = Product.objects.filter(isActive=True)  # Fetching products instead of services
            serializer = ProductSerializer(products, many=True, context={'request': request})
            return Response({
                'success': True,
                'message': 'Products retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProductList(APIView):

    def get(self, request, format=None):
        try:
            products = Product.objects.all() # Fetching products instead of services
            serializer = ProductSerializer(products, many=True, context={'request': request})
            return Response({
                'success': True,
                'message': 'Products retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class JobsList(APIView):

    def get(self, request, format=None):
        try:
            jobs = Job.objects.all()
            serializer = JobSerializer(jobs, many=True, context={'request': request})
            return Response({
                'success': True,
                'message': 'Jobs retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class JobApplicationView(APIView):
    def post(self, request):
        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            job_application = serializer.save()
            # Construct full URL for resume_url
            resume_full_url = request.build_absolute_uri(job_application.resume_url)

            return Response(
                {
                    "message": "Job application submitted successfully!",
                    "resume_url": resume_full_url  # Return full resume URL
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class BlogList(APIView):
    def get(self, request, format=None):
        try:
            blogs = BlogPost.objects.prefetch_related('images').all()  # Optimize query with prefetch_related
            serializer = BlogSerializer(blogs, many=True, context={'request': request})
            return Response({
                'success': True,
                'message': 'Blogs retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CommentView(APIView):
    def post(self, request):
        blog_comment_id = request.data.get('blog_comment')

        if not blog_comment_id:
            return Response(
                {"success": False, "message": "Blog comment ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(blog_comment_id=blog_comment_id)
            
            return Response(
                {
                    'success': True,
                    "message": "Comment added successfully!",
                    'data':serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CommentList(APIView):

    def get(self, request, blog_post_id=None, format=None):
        try:
            # Check if a blog_post_id was provided
            if blog_post_id:
                # Retrieve comments for the specific blog post
                comments = Comment.objects.filter(blog_comment_id=blog_post_id)
            else:
                # Retrieve all comments if no blog_post_id is provided
                comments = Comment.objects.all()

            serializer = CommentSerializer(comments, many=True, context={'request': request})
            return Response({
                'success': True,
                'message': 'Comments retrieved successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class LikeView(APIView):
    def post(self, request, blog_post_id):
        try:
            blog_post = BlogPost.objects.get(id=blog_post_id)
            # Increment the likes
            if blog_post.likes is None:
                blog_post.likes = 0
            blog_post.likes += 1
            blog_post.save()

            return Response(
                {
                    'success': True,
                    'message': 'Like added successfully!',
                    'likes': blog_post.likes
                },
                status=status.HTTP_200_OK
            )
        except BlogPost.DoesNotExist:
            return Response(
                {'success': False, 'message': 'Blog post not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'success': False, 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class ViewCountView(APIView):
    def post(self, request, blog_post_id):
        try:
            blog_post = BlogPost.objects.get(id=blog_post_id)
            # Increment the views
            if blog_post.views is None:
                blog_post.views = 0
            blog_post.views += 1
            blog_post.save()

            return Response(
                {
                    'success': True,
                    'message': 'View count updated successfully!',
                    'views': blog_post.views
                },
                status=status.HTTP_200_OK
            )
        except BlogPost.DoesNotExist:
            return Response(
                {'success': False, 'message': 'Blog post not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'success': False, 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class UserRegisterView(APIView):
    def post(self, request):
        # Extract the username and phone from the request data
        username = request.data.get('username')
        phone = request.data.get('phone')

        # Check if the user already exists
        user = CustomUser.objects.filter(username=username, phone=phone).first()
        
        if user:
            # User exists, log them in
            login(request, user)  # Log the user in
            return Response({
                'success': True,
                'message': 'Logged in successfully.',
                'data': {
                    'id':user.id,
                    'username': user.username,
                    'phone': user.phone,
                   

                }
            }, status=status.HTTP_200_OK)
        
        # User does not exist, create a new user
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)  # Log the new user in
            return Response({
                'success': True,
                'message': 'Registered successfully and logged in.',
                'data': {
                    'id':user.id,
                    'username': user.username,
                    'phone': user.phone,
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'message': 'Registration failed.',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)




class QuestionAndAnswerView(APIView):
    def post(self, request):
        print("Incoming request data:", request.data)
        serializer = QuestionAndAnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Question and answer saved successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Failed to save question and answer.',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)