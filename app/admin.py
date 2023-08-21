from django.contrib import admin
from app.models import User, Category, Blog

# Register your models here.
admin.site.register([User, Blog, Category])