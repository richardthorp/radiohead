from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from ..models import PortalTextPost, PortalImagesPost, PortalVideoPost
from profiles.models import Profile


class TestPortalViews(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='test_user',
            email='test_user@email.com',
            password='test_password'
            )
        self.text_post = PortalTextPost.objects.create(
            title='test_text_post',
            post_blurb='Test blurb',
            lead_image='test-image.jpg',
            lead_image_summary='Test summary',
            text_content='Test text content',
        )
        self.video_post = PortalVideoPost.objects.create(
            title='test_text_post',
            post_blurb='Test blurb',
            lead_image='test-image.jpg',
            lead_image_summary='Test summary',
            video_url='http://www.test-url.com',
            text_content='Test text content',
        )
        self.images_post = PortalImagesPost.objects.create(
            title='test_text_post',
            post_blurb='Test blurb',
            lead_image='test-image.jpg',
            lead_image_summary='Test summary',
            text_content='Test text content',
            image_1='test-image.jpg',
            image_1_summary='test summary',
            image_2='test-image.jpg',
            image_2_summary='test summary',
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

    def test_get_portal_content_page_filter_text(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.profile.subscription_status = 'active'
        user.profile.save()
        url = reverse('portal_content')
        response = self.client.post(url, data={'filter': 'text'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['posts']), 1)
        correct_model_instance = isinstance(response.context['posts'][0],
                                            PortalTextPost)
        self.assertTrue(correct_model_instance)

    def test_get_portal_content_page_filter_videos(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.profile.subscription_status = 'active'
        user.profile.save()
        url = reverse('portal_content')
        response = self.client.post(url, data={'filter': 'videos'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['posts']), 1)
        correct_model_instance = isinstance(response.context['posts'][0],
                                            PortalVideoPost)
        self.assertTrue(correct_model_instance)

    def test_get_portal_content_page_filter_images(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.profile.subscription_status = 'active'
        user.profile.save()
        url = reverse('portal_content')
        response = self.client.post(url, data={'filter': 'images'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['posts']), 1)
        correct_model_instance = isinstance(response.context['posts'][0],
                                            PortalImagesPost)
        self.assertTrue(correct_model_instance)

    def test_get_portal_content_without_subscription_redirects(self):
        self.client.login(username='test_user', password='test_password')
        url = reverse('portal_content')
        response = self.client.get(url)
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        # Credit to Cédric Julien on Stack Overflow for this function to
        # remove whitepace from a string and add spaces
        # https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string
        formatted_message = " ".join(str(messages[0]).split())
        expected_string = 'Sorry, you must have an active subscription to \
            Portal to view this page.'
        formatted_expected_string = " ".join(expected_string.split())
        self.assertEqual(formatted_message, formatted_expected_string)
        self.assertRedirects(response, reverse('portal_info'))

    def test_user_must_be_logged_in_to_view_portal_text_post_detail(self):
        self.client.login(username='test_user', password='test_password')
        url = reverse('portal_post_detail', args=['text', self.text_post.slug])
        response = self.client.get(url)
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        # See whitespace removal function credit in test above
        formatted_message = " ".join(str(messages[0]).split())
        expected_string = 'Sorry, you must have an active subscription to \
            Portal to view this page.'
        formatted_expected_string = " ".join(expected_string.split())
        self.assertEqual(formatted_message, formatted_expected_string)
        self.assertRedirects(response, reverse('portal_info'))

    def test_get_text_post_detail_page_with_active_subscriber(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.profile.subscription_status = 'active'
        user.profile.save()
        url = reverse('portal_post_detail', args=['text', self.text_post.slug])
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'portal/text_post.html')

    def test_get_video_post_detail_page_with_active_subscriber(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.profile.subscription_status = 'active'
        user.profile.save()
        url = reverse('portal_post_detail',
                      args=['video', self.video_post.slug])
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'portal/video_post.html')

    def test_get_images_post_detail_page_with_active_subscriber(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.profile.subscription_status = 'active'
        user.profile.save()
        url = reverse('portal_post_detail',
                      args=['images', self.images_post.slug])
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'portal/images_post.html')
