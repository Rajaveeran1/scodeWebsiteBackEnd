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
            'authorImage', 'created_at', 'images','role'
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'blog_comment', 'user_name', 'comment']


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone']

    def validate_phone(self, value):
        if CustomUser.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone number is already registered.")
        return value

    def create(self, validated_data):
        # Create user without a password (this may have security implications)
        return CustomUser.objects.create(**validated_data)
    

class QuestionAndAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAndAnswer
        fields = ['user', 'question', 'Answer']

    def validate_user(self, value):
        # Optionally, validate that the user exists
        if not CustomUser.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("User does not exist.")
        return value


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'image']