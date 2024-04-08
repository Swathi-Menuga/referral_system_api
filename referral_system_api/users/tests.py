from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.client.login(username='testuser', password='password123')
        self.registration_success_url = reverse('registration_success', kwargs={'user_id': self.user.id})
    
    def test_registration_success_view(self):
        response = self.client.get(self.registration_success_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Registration Success')
        self.assertTemplateUsed(response, 'registration_success.html')

class UserDetailsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.client.login(username='testuser', password='password123')
    
    def test_user_details_view(self):
        response = self.client.get(reverse('user_details'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.email)
        # Add more assertions for other user details as needed
        self.assertTemplateUsed(response, 'user_details.html')

class ReferralsEndpointTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.login(username='testuser', password='password123')
    
    def test_referrals_endpoint_view(self):
        # Make a GET request to the referrals endpoint
        response = self.client.get(reverse('referrals_endpoint'))
        
        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Check if the correct template is used
        self.assertTemplateUsed(response, 'referrals.html')
        
        # Check if the page contains the user's referral code message
        self.assertContains(response, 'You do not have a referral code.')
        
        # Check if the page contains the paginated referrals
        self.assertTrue('page_obj' in response.context)