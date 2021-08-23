from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User


class TestHomeView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             email='test_user@email.com',
                                             password='test_password')

    def test_get_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_get_admin_page_as_staff_returns_admin_hub(self):
        self.client.login(username='test_user',
                          password='test_password')
        self.user.is_staff = True
        self.user.save()
        url = reverse('admin_hub')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('home/admin-hub.html')

    def test_get_admin_page_as_normal_user_redirects(self):
        self.client.login(username='test_user',
                          password='test_password')
        url = reverse('admin_hub')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
