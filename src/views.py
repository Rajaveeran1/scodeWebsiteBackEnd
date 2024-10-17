from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

   
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