
from django.urls import path
from .views import *

app_name = "main"   


urlpatterns = [
    path("", homepage, name="homepage"),

    path("register", RegisterStudentView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", logout_request, name= "logout"),
    path("password_reset", password_reset_request, name="password_reset"),
    path("view_profile", view_profile, name="view_profile"),
    path("edit_profile", edit_profile, name="edit_profile"),
    
    path("course_create",CourseCreateView.as_view(),name="course_create"),
    path("course_join",course_join,name="course_join"),
    path("join_course/<uidb64>/<token>/<course_id>",join_course,name="join_course"),
    path('view_couse/<str:id>', course_single, name='view_course'),
    path('manual_grade/<str:id>', manual_grade, name='manual_grade'),
    path('manual_grade_all/<str:name>/<str:title>', manual_grade_all, name="manual_grade_all"),
    
    path('create_assignment/<str:id>/', AssignmentCreateView.as_view(), name='create_assignment'),
    path('submit_assignment/<int:id>/', AssignmentSubmissionView.as_view(), name='submit_assignment'),
    path('view_submissions/<str:name>/<str:title>/<parent>', AssignmentSubmissionListView.as_view(), name='view_submissions'),
]