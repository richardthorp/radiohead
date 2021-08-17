from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from profiles.models import Profile


class TestPortalViews(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='test_user',
            email='test_user@email.com',
            password='test_password'
            )

    def test_get_portal_info_page_with_subscribed_user(self):
        self.client.login(username='test_user', password='test_password')
        url = reverse('portal_info')
        user = User.objects.get(username='test_user')
        user.profile.subscription_status = 'active'
        user.profile.save()
        response = self.client.get(url)
        self.assertRedirects(response, reverse('portal_content'))

    def test_get_portal_info_page_with_signed_in_non_subscribed_user(self):
        self.client.login(username='test_user', password='test_password')
        url = reverse('portal_info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('portal/portal_info.html')

    def test_get_portal_info_page_with_anonymous_user(self):
        url = reverse('portal_info')
        # self.client.login(username='test_user', password='test_password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('portal/portal_info.html')
