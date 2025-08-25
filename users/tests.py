from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

# VIEW TESTS

class UsersViewTests(TestCase):
    """Tests for the views in the users app."""

    def setUp(self):
        """Set up a client and some user data for testing."""
        self.client = Client()
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        self.logout_url = reverse('users:logout')
        self.accounts_url = reverse('account_logs:account_logs')
        
        # A user that already exists for login tests
        self.existing_user = User.objects.create_user(
            username='testuser', 
            password='password123'
        )

    def test_register_page_loads(self):
        """Test that the registration page loads correctly with a GET request."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, 'Create Your Account')

    def test_successful_user_registration(self):
        """Test that a user can be successfully created with a POST request."""
        # The default UserCreationForm has 'username', 'password', and 'password2'
        registration_data = {
            'username': 'successfuluser',
            'password1': 'sheikhhasinaranawayin2024',
            'password2': 'sheikhhasinaranawayin2024'
        }

        response = self.client.post(self.register_url, registration_data)
        
        # A successful registration logs the user in and redirects to the index page.
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account_logs:index'))
        
        # Check that the user was actually created in the database.
        self.assertTrue(User.objects.filter(username='successfuluser').exists())

    def test_registration_with_password_mismatch(self):
        """Test that registration fails if passwords do not match."""
        registration_data = {
            'username': 'mismatchuser',
            'password1': 'sheikhhasinaranawayin2024',
            'password2': 'sheikhhasinaranawayin2025'
        }
        response = self.client.post(self.register_url, registration_data)
        
        # The page should re-render with an error message.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The two password fields didn’t match.')
        
        # Ensure the user was NOT created.
        self.assertFalse(User.objects.filter(username='mismatchuser').exists())

    def test_login_page_loads(self):
        """Test that the login page loads correctly with a GET request."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, 'Log In to Your Account')

    def test_successful_login(self):
        """Test that an existing user can log in."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        # A successful login should redirect to the accounts page.
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.accounts_url)
        
        # confirm the user is logged in
        response = self.client.get(self.accounts_url)
        self.assertContains(response, 'Hello, testuser')

    def test_unsuccessful_login(self):
        """Test that login fails with incorrect credentials."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        # Should re-render the login page with an error.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password.')

    def test_logout_view(self):
        """Test that a logged-in user can log out."""
        # log the user in.
        self.client.login(username='testuser', password='password123')
        
        # Check that the user is logged in by accessing a protected page.
        response = self.client.get(self.accounts_url)
        self.assertEqual(response.status_code, 200)
        
        # log the user out.
        response = self.client.post(self.logout_url)
        
        # A successful logout should redirect to the homepage as per settings.py
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account_logs:index'))
        
        # Follow the redirect to the homepage and check its content.
        response = self.client.get(response.url)
        self.assertContains(response, 'Account Expense Tracker') # Check for homepage content.
        
        # confirm the user is logged out by trying to access a protected page again.
        response = self.client.get(self.accounts_url)
        self.assertEqual(response.status_code, 302) # Should redirect to login.
        self.assertRedirects(response, f'{self.login_url}?next={self.accounts_url}')