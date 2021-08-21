from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from checkout.models import Order


class TestProfileView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@email.com',
            password='test_password'
        )
        self.order = Order.objects.create(
            email='test@email.com',
            name='Test User',
            phone_number='12345678901',
            address_line1='Test Line 1',
            town_or_city='Test Town',
            country='GB'
            )

    def test_get_profile_page(self):
        self.client.login(username='test_user', password="test_password")
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_get_order_history_page(self):
        self.client.login(username='test_user', password="test_password")
        url = reverse('order_history', args=[self.order.order_number])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')

    def test_save_profile_form_returns_message(self):
        self.client.login(username='test_user', password="test_password")
        url = reverse('profile')
        response = self.client.post(url, data={'default_name': True})

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Profile updated")
