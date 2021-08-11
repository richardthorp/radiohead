from django.test import TestCase
from django.contrib.auth.models import User


class TestModels(TestCase):
    def test_profile_str_method(self):
        user = User.objects.create_user(
            username='test_user',
            email='test_user@email.com',
            password='test_password'
        )

        self.assertEqual(str(user.profile), "test_user's Profile")
