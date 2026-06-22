from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class SimpleTests(TestCase):

    def test_home_page_status(self):
        # 1. ამოწმებს, იხსნება თუ არა მთავარი გვერდი
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_status(self):
        # 2. ამოწმებს, იხსნება თუ არა ლოგინის გვერდი
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_user_model_count(self):
        # 3. ამოწმებს, იქმნება თუ არა იუზერი ბაზაში
        User.objects.create_user(username='testuser', password='password123')
        self.assertEqual(User.objects.count(), 1)
