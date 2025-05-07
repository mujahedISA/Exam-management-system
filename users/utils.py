# utils.py
import string, random
from django.contrib.auth.models import User, Group
from .models import StudentProfile  

def generate_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_student_account(email, name, program):
    if User.objects.filter(email=email).exists():
        return None, "Student already exists"

    password = generate_password()
    first_name, *last_name_parts = name.strip().split()
    last_name = " ".join(last_name_parts) if last_name_parts else ""

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    student_group, _ = Group.objects.get_or_create(name='student')
    user.groups.add(student_group)

    StudentProfile.objects.create(
        user=user,
        program=program,
        generated_password=password
    )

    return {
        "email": email,
        "name": name,
        "program": program,
        "password": password,
    }, None
