from django.urls import path
from . import views

urlpatterns = [
  
    path('studentgrade/', views.studentgrade, name='studentgrade'),
    
    path('resitgrades/', views.resitgrades, name='resitgrades'),
    path('insexam/', views.insexam, name='insexam'),      
    path('declare_resit/', views.declare_resit, name='declare_resit'),
    path('delete_grade/', views.delete_grade, name='delete_grade'),
    path('upload_grades/<int:course_id>/', views.upload_grades, name='upload_grades'),
    path('exams/download_resit_excel/', views.download_resit_excel, name='download_resit_excel'),


    
  
]