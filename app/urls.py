from app.views import HomeView, LoginView, SignUpView, PatientDashboardView, DoctorDashboardView, BlogEditorView, MyBlogsView, ViewBlogView, EditBlogView, DeleteBlogView, PublishBlogView, AllBlogsView, BlogDetailsView
from django.urls import path

urlpatterns = [
    path("", HomeView.as_view(), name="homepage"),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),

    path("patient/", PatientDashboardView.as_view(), name="patient"),
    path("patient/all-blogs/", AllBlogsView.as_view(), name="all-blogs"),
    path("patient/filter-blogs/<int:id>/", AllBlogsView.as_view(), name="cat-filter"),
    path("patient/blog-details/<int:id>/", BlogDetailsView.as_view(), name="blog-details"),

    path("doctor/", DoctorDashboardView.as_view(), name="doctor"),
    path("doctor/blog-editor/", BlogEditorView.as_view(), name="blog-editor"),
    path("doctor/my-blogs/", MyBlogsView.as_view(), name="my-blogs"),
    path("doctor/view-blog/<int:id>/", ViewBlogView.as_view(), name="view-blog"),
    path("doctor/edit-blog/<int:id>/", EditBlogView.as_view(), name="edit-blog"),
    path("doctor/delete-blog/<int:id>/", DeleteBlogView.as_view(), name="delete-blog"),
    path("doctor/publish-blog/<int:id>/", PublishBlogView.as_view(), name="publish-blog"),
]
