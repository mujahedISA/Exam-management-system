
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random
import string
from django.http import JsonResponse
import openpyxl
from courses.models import Announcement
from users.utils import create_student_account
from .models import StudentProfile
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


@csrf_exempt  # Remove in production
def add_student(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        program = request.POST.get("program")

        student_data, error = create_student_account(email, name, program)
        if error:
            return JsonResponse({"status": "error", "message": error})

        return JsonResponse({
            "status": "success",
            **student_data
        })

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


@csrf_exempt
def upload_excel_students(request):
    if request.method == "POST" and request.FILES.get("file"):
        excel_file = request.FILES["file"]
        wb = openpyxl.load_workbook(excel_file)
        ws = wb.active

        created_students = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            email, name, program = row
            student_data, error = create_student_account(email, name, program)
            if student_data:
                created_students.append(student_data)
            # Optionally log errors for duplicates

        return JsonResponse({"status": "success", "students": created_students})

    return JsonResponse({"status": "error", "message": "Invalid request"})


@csrf_exempt  # Remove in production
def delete_student(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            user.delete()
            return JsonResponse({"status": "success"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Student not found"})

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

@csrf_exempt  # Remove in production
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email'].strip().lower()  # lower it
        password = request.POST['password']

        # Since we saved username=email.lower(), we can authenticate using email
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)

            # Check user's group to redirect
            if user.groups.filter(name__iexact='student').exists():
                return redirect('student_page')
            elif user.groups.filter(name__iexact='instructor').exists():
                return redirect('instructor_page')
            elif user.groups.filter(name__iexact='faculty').exists():
                return redirect('faculty_page')
            else:
                return render(request, 'index.html', {'error': 'User has no group assigned.'})

        else:
            return render(request, 'index.html', {'error': 'Invalid email or password.'})

    return render(request, 'index.html')


@login_required
def student_page(request):
    announcements = Announcement.objects.order_by('-created_at')  # Or [:3] if you want a few
    return render(request, 'studentpage.html', {
        'announcements': announcements
         })

@login_required
def instructor_page(request):
    announcements = Announcement.objects.filter(posted_by__groups__name='faculty').order_by('-created_at')
    return render(request, 'instroctorpage.html', {
        'announcements': announcements
         })

@login_required
def faculty_page(request):
    return render(request, 'facultysecpage.html')


def faculty_payment(request):
    students = StudentProfile.objects.select_related('user').all()
    page_number = request.GET.get('page', 1)
    per_page = 5  # Or allow request.GET.get('per_page', 10) to be dynamic

    paginator = Paginator(students, per_page)
    page_obj = paginator.get_page(page_number)

    context = {
        'students': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'facultypaymentmanagement.html', context)


def forget(request):
    return render(request, 'forget.html')

