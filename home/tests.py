# Home app tests
from django.test import TestCase

# Create your tests here.
class BasicTestCase(TestCase):
    def test_landing_page(self):
        """Test that the landing page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_irc_client_page(self):
        """Test that the IRC client page loads"""
        response = self.client.get('/irc/')
        self.assertEqual(response.status_code, 200)
