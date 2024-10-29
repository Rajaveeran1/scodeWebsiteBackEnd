from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, phone, **extra_fields):
        if not username:
            raise ValueError("The Username field is required.")
        if not phone:
            raise ValueError("The Phone field is required.")
        
        user = self.model(username=username, phone=phone, **extra_fields)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Add a unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Add a unique related_name
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.username



class QuestionAndAnswer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users')
    question = models.CharField(max_length=255)
    Answer = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class Service(models.Model):
    title = models.CharField(max_length=200)
    animation = models.CharField(max_length=50)
    imageUrl = models.ImageField(upload_to='service_images/', null=True, blank=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    title_description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products_images/', null=True, blank=True)
    short_description = models.TextField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    animation = models.CharField(max_length=50)
    isActive = models.BooleanField(default=False)
    def __str__(self):
        return self.title
       

class ProductImage(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to='products_images/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.product.title
    

class Internship(models.Model):
    title = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    class_mode = models.CharField(max_length=100)
    class_hour = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    description = models.JSONField()  # JSONField for storing list data
    animation = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    

class Job(models.Model):
    title = models.CharField(max_length=200)
    experience = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.JSONField()  # JSONField for storing list data
    animation = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    

class ActiveProject(models.Model):
    title = models.CharField(max_length=200)
    animation = models.CharField(max_length=50)
    imageUrl = models.ImageField(upload_to='service_images/', null=True, blank=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    job_title = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @property
    def resume_url(self):
        if self.resume:
            return self.resume.url  # This is the relative URL, we will handle full URL in the view
        return None

from ckeditor.fields import RichTextField

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/')
    content = RichTextField()  # Changed to RichTextField
    author = models.CharField(max_length=200)
    views = models.IntegerField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    authorImage = models.ImageField(
        upload_to='author_images/',
        default='author_images/default_author.png'  # Path to default image
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class BlogImage(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', null=True,blank=True)
    caption = models.CharField(max_length=255, blank=True)
    content =  RichTextField( null=True,blank=True)
    # code_snippet_title = models.CharField(max_length=255, blank=True)
    code_snippet = models.TextField(blank=True, null=True)
    index_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Image for {self.blog_post.title}"
    
class Comment(models.Model):
    blog_comment = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255, blank=True)
    comment = models.CharField(max_length=255, blank=True)
    

    def __str__(self):
        return f"Cpmment for {self.blog_comment.title}"