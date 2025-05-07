from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from exams.models import Course
from .models import Announcement

@csrf_exempt  # for simplicity; better to use CSRF properly

def post_announcement(request):
    if request.method == "POST":
        title = request.POST.get("title")
        text = request.POST.get("text")

        if not title or not text:
            return JsonResponse({"status": "error", "message": "Missing title or text"})

        # Save announcement and track who posted it
        Announcement.objects.create(
            title=title,
            text=text,
            posted_by=request.user
        )

        return JsonResponse({"status": "success"})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
def student_announcements(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'student_announcements.html', {"announcements": announcements})

def instructor_home(request):
    announcements = Announcement.objects.filter(posted_by__groups__name='faculty').order_by('-created_at')
    return render(request, 'instructor_home.html', {
        'announcements': announcements
    })



def insanno(request):
    return render(request, 'insanno.html')

def facultysecanoun(request):
    return render(request, 'facultysec-anoun.html')

def insresitexam(request):
    courses = Course.objects.all()
    return render(request, 'insresitexam.html', {'courses': courses})
    