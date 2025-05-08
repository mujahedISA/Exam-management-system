
# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from exams.models import Course
from .models import Announcement
import json

class AnnouncementModelTests(TestCase):
    def setUp(self):
        # Creating a test user for model tests
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_announcement_creation(self):
        """Test creating an announcement with valid data"""
        announcement = Announcement.objects.create(
            title="Test Announcement",
            text="This is a test announcement",
            posted_by=self.user
        )
        self.assertEqual(announcement.title, "Test Announcement")
        self.assertEqual(announcement.text, "This is a test announcement")
        self.assertEqual(announcement.posted_by, self.user)
        self.assertIsNotNone(announcement.created_at)
        self.assertEqual(str(announcement), "Test Announcement")

    def test_announcement_without_posted_by(self):
        """Test creating an announcement with null posted_by"""
        announcement = Announcement.objects.create(
            title="Test Announcement",
            text="This is a test announcement",
            posted_by=None
        )
        self.assertIsNone(announcement.posted_by)

    def test_title_max_length(self):
        """Test that title respects max_length constraint"""
        max_length = Announcement._meta.get_field('title').max_length
        long_title = "x" * (max_length + 1)
        with self.assertRaises(Exception):
            Announcement.objects.create(
                title=long_title,
                text="Test text",
                posted_by=self.user
            )

class AnnouncementViewTests(TestCase):
    def setUp(self):
        # Set up test client and users
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.faculty_user = User.objects.create_user(username='faculty', password='facultypass123')
        
        # Create faculty group and add faculty user
        faculty_group = Group.objects.create(name='faculty')
        self.faculty_user.groups.add(faculty_group)
        
        # Create test announcement
        self.announcement = Announcement.objects.create(
            title="Test Announcement",
            text="This is a test announcement",
            posted_by=self.faculty_user
        )

    def test_post_announcement_view_authenticated(self):
        """Test posting an announcement when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('post_announcement'),
            {'title': 'New Announcement', 'text': 'Announcement content'},
            content_type='application/x-www-form-urlencoded'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {'status': 'success'}
        )
        self.assertTrue(Announcement.objects.filter(title='New Announcement').exists())

    def test_post_announcement_missing_fields(self):
        """Test posting an announcement with missing fields"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('post_announcement'),
            {'title': 'Only Title'},
            content_type='application/x-www-form-urlencoded'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {'status': 'error', 'message': 'Missing title or text'}
        )

    def test_post_announcement_invalid_method(self):
        """Test post_announcement with invalid HTTP method"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('post_announcement'))
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {'status': 'error', 'message': 'Invalid request method'}
        )

    def test_student_announcements_view(self):
        """Test student_announcements view renders correctly"""
        response = self.client.get(reverse('student_announcements'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_announcements.html')
        self.assertContains(response, "Test Announcement")
        self.assertIn('announcements', response.context)
        self.assertEqual(len(response.context['announcements']), 1)

    def test_instructor_home_view(self):
        """Test instructor_home view for faculty announcements"""
        response = self.client.get(reverse('instructor_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instructor_home.html')
        self.assertContains(response, "Test Announcement")
        self.assertIn('announcements', response.context)
        self.assertEqual(len(response.context['announcements']), 1)

    def test_insanno_view(self):
        """Test insanno view renders correctly"""
        response = self.client.get(reverse('insanno'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'insanno.html')

    def test_facultysecanoun_view(self):
        """Test facultysecanoun view renders correctly"""
        response = self.client.get(reverse('facultysecanoun'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'facultysec-anoun.html')

    def test_insresitexam_view(self):
        """Test insresitexam view with courses"""
        # Create a test course
        Course.objects.create(name="Test Course", code="TC101")
        response = self.client.get(reverse('insresitexam'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'insresitexam.html')
        self.assertIn('courses', response.context)
        self.assertEqual(len(response.context['courses']), 1)
        self.assertContains(response, "Test Course")
