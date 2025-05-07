from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('add_student/', views.add_student, name='add_student'),
    path('student/', views.student_page, name='student_page'),
    path('forget/', views.forget, name='forget'),
    path('instructor/', views.instructor_page, name='instructor_page'),
    path('faculty/', views.faculty_page, name='faculty_page'),
    path('faculty/payment/', views.faculty_payment, name='faculty_payment'),
    path('delete_student/', views.delete_student, name='delete_student'),
    path('upload_excel/', views.create_student_account, name='create_student_account'),
    path('upload_excel_students/', views.upload_excel_students, name='upload_excel_students'),
    
]
