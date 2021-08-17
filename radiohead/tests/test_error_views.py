from django.test import TestCase
from django.shortcuts import reverse


class TestErrorViews(TestCase):
    def test_404_page(self):
        url = reverse('home') + 'bad_link_string'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed('templates/404_page.html')
