from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Internship, Job, Service, Product, ProductImage,JobApplication

# Unregister the default Group and User models from the admin
admin.site.unregister(Group)
admin.site.unregister(User)

# Register your models
admin.site.register(Internship)
admin.site.register(Job)
admin.site.register(Service)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(JobApplication)

