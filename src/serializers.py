from rest_framework import serializers
from .models import *

class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = ['id', 'title', 'duration', 'class_mode', 'class_hour', 'location', 'description', 'animation']


class ServiceSerializer(serializers.ModelSerializer):
    imageUrl = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id', 'title', 'imageUrl', 'animation']

    def get_imageUrl(self, obj):
        request = self.context.get('request')
        if obj.imageUrl:
            return request.build_absolute_uri(obj.imageUrl.url)
        return None
    


class ProductImageSerializer(serializers.ModelSerializer):
    imageUrl = serializers.ImageField(source='image', read_only=True)  # Adjusting field name

    class Meta:
        model = ProductImage
        fields = ('id', 'title', 'imageUrl', 'description')  # Adjust field names if necessary


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, source='product_image', read_only=True)  # Related images
    title_desc = serializers.CharField(source='title_description')  # Adjusting field name
    imageUrl = serializers.ImageField(source='image', read_only=True) 

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'title_desc',
            'imageUrl',
            'long_description',  # No need for source
            'short_description',  # No need for source
            'images',
            'animation',
            'isActive',
        )


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'experience', 'location', 'description', 'animation']


class JobApplicationSerializer(serializers.ModelSerializer):
    resume_url = serializers.ReadOnlyField()  # Expose the resume public URL

    class Meta:
        model = JobApplication
        fields = ['name', 'email', 'phone', 'message', 'resume', 'resume_url', 'job_title']
        read_only_fields = ['resume_url']



class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'image', 'caption', 'content', 'code_snippet','index_id']

class BlogSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True, read_only=True)  # Nesting BlogImageSerializer

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'image', 'author', 'content','views','likes', 
            'authorImage', 'created_at', 'images'
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'blog_comment', 'user_name', 'comment']