"""
Tests for the Django API application.
Run with: python manage.py test api.tests -v 2
"""

from django.test import TestCase, Client
from django.urls import reverse
from api.models import Student


class StudentModelTests(TestCase):
    """Test cases for the Student model."""
    
    def test_create_student(self):
        """Test creating a student instance."""
        student = Student.objects.create(
            name="Test Student",
            email="test@example.com",
            role="student"
        )
        self.assertEqual(student.name, "Test Student")
        self.assertEqual(student.email, "test@example.com")
        self.assertEqual(student.role, "student")
        self.assertTrue(student.is_active)
    
    def test_student_str(self):
        """Test the __str__ method returns name with role."""
        student = Student.objects.create(
            name="Alice",
            email="alice@example.com",
            role="student"
        )
        self.assertEqual(str(student), "Alice (student)")
    
    def test_student_email_unique(self):
        """Test that email must be unique."""
        Student.objects.create(
            name="First",
            email="unique@example.com",
            role="student"
        )
        # Creating another with same email should raise IntegrityError
        with self.assertRaises(Exception):
            Student.objects.create(
                name="Second",
                email="unique@example.com",  # Same email
                role="teacher"
            )


class StudentAPITests(TestCase):
    """Test cases for the Student API endpoints."""
    
    def setUp(self):
        """Set up test data before each test."""
        self.client = Client()
        self.student = Student.objects.create(
            name="Test Student",
            email="test@example.com",
            role="student"
        )
    
    def test_student_list_get(self):
        """Test GET /api/students/ returns list of students."""
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Test Student")
    
    def test_student_list_post(self):
        """Test POST /api/students/ creates a new student."""
        import json
        response = self.client.post(
            '/api/students/',
            data=json.dumps({
                'name': 'New Student',
                'email': 'new@example.com',
                'role': 'student'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        
        # Check the response data
        data = response.json()
        self.assertEqual(data['name'], 'New Student')
        self.assertEqual(data['email'], 'new@example.com')
        
        # Check it was actually saved to database
        self.assertEqual(Student.objects.count(), 2)
    
    def test_student_detail_get(self):
        """Test GET /api/students/{id}/ returns a single student."""
        response = self.client.get(f'/api/students/{self.student.id}/')
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['id'], self.student.id)
        self.assertEqual(data['name'], "Test Student")
    
    def test_student_detail_not_found(self):
        """Test GET /api/students/{id}/ with invalid ID returns 404."""
        response = self.client.get('/api/students/9999/')
        self.assertEqual(response.status_code, 404)
    
    def test_student_update_put(self):
        """Test PUT /api/students/{id}/ updates a student."""
        import json
        response = self.client.put(
            f'/api/students/{self.student.id}/',
            data=json.dumps({
                'name': 'Updated Name',
                'email': 'updated@example.com',
                'role': 'teacher'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Refresh from database
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, 'Updated Name')
        self.assertEqual(self.student.role, 'teacher')
    
    def test_student_delete(self):
        """Test DELETE /api/students/{id}/ removes a student."""
        response = self.client.delete(f'/api/students/{self.student.id}/')
        self.assertEqual(response.status_code, 204)
        
        # Check it was deleted
        self.assertEqual(Student.objects.count(), 0)


class AdminTests(TestCase):
    """Test cases for Django admin functionality."""
    
    def setUp(self):
        """Create admin user and client."""
        from django.contrib.auth.models import User
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
    
    def test_admin_login(self):
        """Test admin login works."""
        response = self.client.post('/admin/login/', {
            'username': 'admin',
            'password': 'adminpass123'
        })
        # Should redirect to admin index
        self.assertEqual(response.status_code, 302)
    
    def test_admin_requires_login(self):
        """Test admin page requires authentication."""
        response = self.client.get('/admin/')
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)


# UNCOMMENT FOR AUTH EXERCISE:
# class AuthTests(TestCase):
#     """Test cases for authentication (when auth is enabled)."""
#     
#     def setUp(self):
#         """Set up test data."""
#         from django.contrib.auth.models import User
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='testuser',
#             password='testpass123'
#         )
#     
#     def test_login_required_redirects(self):
#         """Test that @login_required redirects anonymous users."""
#         response = self.client.get('/api/students/')
#         # When @login_required is enabled, this should redirect to login
#         self.assertEqual(response.status_code, 302)
#     
#     def test_logged_in_user_can_access(self):
#         """Test that logged-in users can access protected endpoints."""
#         self.client.login(username='testuser', password='testpass123')
#         response = self.client.get('/api/students/')
#         # Should work when logged in
#         self.assertEqual(response.status_code, 200)
