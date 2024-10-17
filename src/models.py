from django.db import models

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
