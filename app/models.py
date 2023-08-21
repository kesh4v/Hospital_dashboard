from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=(("Patient", "Patient"), ("Doctor", "Doctor")), blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profile", null=True, blank=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pin = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.first_name:
            return  f"{self.first_name}"
        return self.email
    

class Category(models.Model):
    cat_name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.cat_name
    
class Blog(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="blog-image/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    summary = models.TextField()
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title