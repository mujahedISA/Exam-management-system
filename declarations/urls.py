from django.urls import path
from . import views

urlpatterns = [
    path('resitannouncement/', views.resitannouncement, name='resitannouncement'),
    path('upload_resit_details/<int:course_id>/', views.upload_resit_details, name='upload_resit_details'),
    
    path('facultysecexam/', views.facultysecexam, name='facultysecexam'),
    path('upload_resit_schedule/', views.upload_resit_schedule, name='upload_resit_schedule'),
]
