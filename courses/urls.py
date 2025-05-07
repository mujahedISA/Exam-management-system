from django.urls import path
from . import views

urlpatterns = [

    path('insanno/', views.insanno, name='insanno'),
    path('facultysecanoun/', views.facultysecanoun, name='facultysecanoun'),
    path('post_announcement/', views.post_announcement, name='post_announcement'),
    path('student_announcements/', views.student_announcements, name='student_announcements'),
    path('instructor_home/', views.instructor_home, name='instructor_home'),
    path('insresitexam/', views.insresitexam, name='insresitexam'),
    
]