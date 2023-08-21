from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from app.models import User, Category, Blog
from django.contrib import messages


class BaseView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        
        else:
            # print(request.path.split("/")[1])
            # print(request.user.user_type)
            if request.user.user_type == "Doctor" and request.path.split("/")[1] == "patient":
                return redirect("doctor")
            
            if request.user.user_type == "Patient" and request.path.split("/")[1] == "doctor":
                return redirect("patient")

        return super().dispatch(request, *args, **kwargs)


# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return redirect("login")

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

class PatientDashboardView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, "patient_dashboard.html")
    

class DoctorDashboardView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, "doctor_dashboard.html")
    

class BlogEditorView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, "blog-editor.html", {
            'categories': Category.objects.all()
        })
    
    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        image = request.FILES.get("image")
        category = request.POST.get("category")
        summary = request.POST.get("summary")
        content = request.POST.get("content")

        if title and summary and category and content:

            try:
                blog = Blog()
                blog.title = title
                blog.image = image
                blog.category = Category.objects.get(id=category)
                blog.summary = summary
                blog.content = content
                blog.user = request.user
                blog.save()

                messages.success(request, "Blog Saved!!")
            except:
                messages.error(request, "Something want wrong!!")
        else:
            messages.warning(request, "Submission failed!!")

        return redirect("blog-editor")


class MyBlogsView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, "my-blogs.html", {
            'blogs': Blog.objects.filter(user=request.user),
        })


class AllBlogsView(View):
    def get(self, request, *args, **kwargs):
        cat_id = kwargs.get("id")
        if cat_id:
            return render(request, "all-blogs.html", {
                'blogs': Blog.objects.filter(status=True, category=Category.objects.get(id=cat_id)),
                'categories': Category.objects.all(),
            })
        
        else:
            return render(request, "all-blogs.html", {
                'blogs': Blog.objects.filter(status=True),
                'categories': Category.objects.all(),
            })


class BlogDetailsView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, "blog-details.html", {
            'blog': Blog.objects.get(id=kwargs.get("id")),
        })


class ViewBlogView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, "view-blog.html", {
            'blog': Blog.objects.get(id=kwargs.get("id")),
        })


class EditBlogView(BaseView):
    def get(self, request, *args, **kwargs):
        return render(request, "edit-blog.html", {
            'blog': Blog.objects.get(id=kwargs.get("id")),
            'categories': Category.objects.all(),
        })
    
    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        image = request.FILES.get("image")
        category = request.POST.get("category")
        summary = request.POST.get("summary")
        content = request.POST.get("content")

        if title and summary and category and content:

            try:
                blog = Blog.objects.get(id=kwargs.get("id"), user=request.user)
                blog.title = title
                blog.image = image
                blog.category = Category.objects.get(id=category)
                blog.summary = summary
                blog.content = content
                blog.status = False
                blog.save()

                messages.success(request, "Blog Updated!!")
            except:
                messages.error(request, "Something want wrong!!")
        else:
            messages.warning(request, "Submission failed!!")

        return redirect("doctor")


class DeleteBlogView(BaseView):
    def get(self, request, *args, **kwargs):
        blog = Blog.objects.get(id=kwargs.get("id"))
        blog.delete()
        messages.success(request, "Blog deleted Successfully!!")
        return redirect("doctor")
    

class PublishBlogView(BaseView):
    def get(self, request, *args, **kwargs):
        blog = Blog.objects.get(id=kwargs.get("id"))
        blog.status = True
        blog.save()
        return redirect("my-blogs")


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # print("yo")
            if request.user.user_type == "Doctor":
                return redirect("doctor")
            if request.user.user_type == "Patient":
                return redirect("patient")
        return render(request, "login.html")

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print(user)
        if user == None:
            messages.info(request, 'Enter valid Username or password.')
            print("fail")
            return redirect('login')
        
        else:
            login(request, user)

        messages.success(request, 'You are logged in.')

        if user.user_type == "Patient":
            return redirect("patient")

        if user.user_type == "Doctor":
            return redirect("doctor")

        return redirect('login')



class SignUpView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # print("yo")
            if request.user.user_type == "Doctor":
                return redirect("doctor")
            if request.user.user_type == "Patient":
                return redirect("patient")
        return render(request, "signup.html")

    def post(self, request, *args, **kwargs):
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        type = request.POST.get('user_type')
        username = request.POST.get('username')
        pic = request.FILES.get("profile_pic")
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin = request.POST.get('pin')

        if User.objects.filter(username=username, email=email).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if password != password_confirm:
            messages.error(request, "Password doesn't match!!!")
            return redirect("signup")
        
        user = User()
        user.first_name = fname
        user.last_name = lname
        user.username = username
        user.email = email
        user.profile_pic = pic
        user.address = address
        user.city = city
        user.state = state
        user.user_type = type
        user.pin = pin
        user.set_password(password) 
        user.save()

        messages.success(request, 'Account created successfully')

        print(type)
        login(request, User.objects.get(username=username))
        if type == "Patient":
            return redirect("patient")
        
        if type == "Doctor":
            return redirect("doctor")


        return redirect('signup')