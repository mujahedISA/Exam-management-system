
# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import StudentProfile
from .utils import generate_password, create_student_account
from exams.models import Announcement
import openpyxl
from io import BytesIO

class StudentProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent@example.com', email='teststudent@example.com', password='testpass123')

    def test_student_profile_creation(self):
        """Test creating a StudentProfile with valid data"""
        profile = StudentProfile.objects.create(
            user=self.user,
            program="Computer Science",
            generated_password="abc123"
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.program, "Computer Science")
        self.assertEqual(profile.generated_password, "abc123")
        self.assertEqual(str(profile), "teststudent@example.com")

    def test_program_max_length(self):
        """Test that program respects max_length constraint"""
        long_program = "x" * 101
        with self.assertRaises(Exception):
            StudentProfile.objects.create(
                user=self.user,
                program=long_program,
                generated_password="abc123"
            )

    def test_generated_password_nullable(self):
        """Test that generated_password can be null"""
        profile = StudentProfile.objects.create(
            user=self.user,
            program="Computer Science",
            generated_password=None
        )
        self.assertIsNone(profile.generated_password)

class UtilsTests(TestCase):
    def test_generate_password_length(self):
        """Test generate_password creates password of specified length"""
        password = generate_password(length=10)
        self.assertEqual(len(password), 10)
        self.assertTrue(all(c in (string.ascii_letters + string.digits) for c in password))

    def test_create_student_account_success(self):
        """Test create_student_account with valid data"""
        student_data, error = create_student_account(
            email="newstudent@example.com",
            name="John Doe",
            program="Computer Science"
        )
        self.assertIsNone(error)
        self.assertEqual(student_data['email'], "newstudent@example.com")
        self.assertEqual(student_data['name'], "John Doe")
        self.assertEqual(student_data['program'], "Computer Science")
        self.assertTrue(User.objects.filter(email="newstudent@example.com").exists())
        user = User.objects.get(email="newstudent@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertTrue(user.groups.filter(name='student').exists())
        profile = StudentProfile.objects.get(user=user)
        self.assertEqual(profile.program, "Computer Science")
        self.assertEqual(profile.generated_password, student_data['password'])

    def test_create_student_account_duplicate_email(self):
        """Test create_student_account with duplicate email"""
        User.objects.create_user(
            username="existing@example.com",
            email="existing@example.com",
            password="testpass123"
        )
        student_data, error = create_student_account(
            email="existing@example.com",
            name="Jane Doe",
            program="Mathematics"
        )
        self.assertIsNone(student_data)
        self.assertEqual(error, "Student already exists")

class UsersViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student_user = User.objects.create_user(
            username='student@example.com',
            email='student@example.com',
            password='studentpass123'
        )
        self.instructor_user = User.objects.create_user(
            username='instructor@example.com',
            email='instructor@example.com',
            password='instructorpass123'
        )
        self.faculty_user = User.objects.create_user(
            username='faculty@example.com',
            email='faculty@example.com',
            password='facultypass123'
        )
        self.student_group = Group.objects.create(name='student')
        self.instructor_group = Group.objects.create(name='instructor')
        self.faculty_group = Group.objects.create(name='faculty')
        self.student_user.groups.add(self.student_group)
        self.instructor_user.groups.add(self.instructor_group)
        self.faculty_user.groups.add(self.faculty_group)
        self.student_profile = StudentProfile.objects.create(
            user=self.student_user,
            program="Computer Science"
        )

    def test_login_view_success_student(self):
        """Test login view redirects to student page for student user"""
        response = self.client.post(
            reverse('login'),
            {'email': 'student@example.com', 'password': 'studentpass123'},
            follow=True
        )
        self.assertRedirects(response, reverse('student_page'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_success_instructor(self):
        """Test login view redirects to instructor page for instructor user"""
        response = self.client.post(
            reverse('login'),
            {'email': 'instructor@example.com', 'password': 'instructorpass123'},
            follow=True
        )
        self.assertRedirects(response, reverse('instructor_page'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_success_faculty(self):
        """Test login view redirects to faculty page for faculty user"""
        response = self.client.post(
            reverse('login'),
            {'email': 'faculty@example.com', 'password': 'facultypass123'},
            follow=True
        )
        self.assertRedirects(response, reverse('faculty_page'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_view_invalid_credentials(self):
        """Test login view with invalid credentials"""
        response = self.client.post(
            reverse('login'),
            {'email': 'student@example.com', 'password': 'wrongpass'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Invalid email or password.')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_student_page_view(self):
        """Test student_page view with announcements"""
        self.client.login(username='student@example.com', password='studentpass123')
        announcement = Announcement.objects.create(
            title="Test Announcement",
            text="This is a test",
            posted_by=self.faculty_user
        )
        response = self.client.get(reverse('student_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studentpage.html')
        self.assertIn('announcements', response.context)
        self.assertEqual(len(response.context['announcements']), 1)
        self.assertEqual(response.context['announcements'][0], announcement)

    def test_instructor_page_view(self):
        """Test instructor_page view with faculty announcements"""
        self.client.login(username='instructor@example.com', password='instructorpass123')
        announcement = Announcement.objects.create(
            title="Test Announcement",
            text="This is a test",
            posted_by=self.faculty_user
        )
        response = self.client.get(reverse('instructor_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instroctorpage.html')
        self.assertIn('announcements', response.context)
        self.assertEqual(len(response.context['announcements']), 1)
        self.assertEqual(response.context['announcements'][0], announcement)

    def test_faculty_page_view(self):
        """Test faculty_page view"""
        self.client.login(username='faculty@example.com', password='facultypass123')
        response = self.client.get(reverse('faculty_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'facultysecpage.html')

    def test_faculty_payment_view(self):
        """Test faculty_payment view with pagination"""
        self.client.login(username='faculty@example.com', password='facultypass123')
        response = self.client.get(reverse('faculty_payment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'facultypaymentmanagement.html')
        self.assertIn('students', response.context)
        self.assertIn('page_obj', response.context)
        self.assertIn('paginator', response.context)
        self.assertEqual(len(response.context['students']), 1)
        self.assertEqual(response.context['students'][0], self.student_profile)

    def test_forget_view(self):
        """Test forget view renders correctly"""
        response = self.client.get(reverse('forget'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forget.html')

    def test_add_student_success(self):
        """Test add_student view with valid data"""
        response = self.client.post(
            reverse('add_student'),
            {
                'email': 'newstudent@example.com',
                'name': 'Jane Doe',
                'program': 'Mathematics'
            },
            content_type='application/x-www-form-urlencoded'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                'status': 'success',
                'email': 'newstudent@example.com',
                'name': 'Jane Doe',
                'program': 'Mathematics',
                'password': response.json()['password']
            }
        )
        self.assertTrue(User.objects.filter(email='newstudent@example.com').exists())

    def test_add_student_invalid_method(self):
        """Test add_student view with invalid method"""
        response = self.client.get(reverse('add_student'))
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {'status': 'error', 'message': 'Invalid request method.'}
        )

    def test_delete_student_success(self):
        """Test delete_student view with valid email"""
        response = self.client.post(
            reverse('delete_student'),
            {'email': 'student@example.com'},
            content_type='application/x-www-form-urlencoded'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success'})
        self.assertFalse(User.objects.filter(email='student@example.com').exists())

    def test_delete_student_not_found(self):
        """Test delete_student view with non-existent email"""
        response = self.client.post(
            reverse('delete_student'),
            {'email': 'nonexistent@example.com'},
            content_type='application/x-www-form-urlencoded'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {'status': 'error', 'message': 'Student not found'}
        )

    def test_upload_excel_students_valid(self):
        """Test upload_excel_students with valid Excel file"""
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(['email', 'name', 'program'])
        sheet.append(['newstudent@example.com', 'Jane Doe', 'Mathematics'])
        excel_content = BytesIO()
        workbook.save(excel_content)
        excel_content.seek(0)
        uploaded_file = SimpleUploadedFile(
            "test.xlsx",
            excel_content.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response = self.client.post(
            reverse('upload_excel_students'),
            {'file': uploaded_file},
            format='multipart'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(response.json()['students']), 1)
        self.assertEqual(response.json()['students'][0]['email'], 'newstudent@example.com')
        self.assertTrue(User.objects.filter(email='newstudent@example.com').exists())

    def test_upload_excel_students_duplicate(self):
        """Test upload_excel_students with duplicate email"""
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(['email', 'name', 'program'])
        sheet.append(['student@example.com', 'Jane Doe', 'Mathematics'])
        excel_content = BytesIO()
        workbook.save(excel_content)
        excel_content.seek(0)
        uploaded_file = SimpleUploadedFile(
            "test.xlsx",
            excel_content.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response = self.client.post(
            reverse('upload_excel_students'),
            {'file': uploaded_file},
            format='multipart'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(len(response.json()['students']), 0)  # Duplicate not added
