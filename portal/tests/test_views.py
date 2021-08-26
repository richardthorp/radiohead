from os import unlink
from PIL import Image
import tempfile
from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from ..models import (PortalTextPost, PortalImagesPost, PortalVideoPost,
                      TextPostComment, VideoPostComment, ImagesPostComment)
from profiles.models import Profile


def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGB", size, color)
    image.save(temp_file, 'jpeg')
    return temp_file


class TestPortalViews(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='test_user',
            email='test_user@email.com',
            password='test_password'
            )
        self.test_user_2 = User.objects.create_user(
            username='test_user_2',
            email='test_user_2@email.com',
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
        self.text_post_comment = TextPostComment.objects.create(
            text='Test Text',
            posted_by=self.test_user.profile,
            post=self.text_post
        )
        self.video_post_comment = VideoPostComment.objects.create(
            text='Test Text',
            posted_by=self.test_user.profile,
            post=self.video_post
        )
        self.images_post_comment = ImagesPostComment.objects.create(
            text='Test Text',
            posted_by=self.test_user.profile,
            post=self.images_post
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

    def test_user_must_have_subscription_to_view_portal_text_post_detail(self):
        self.client.login(username='test_user', password='test_password')
        url = reverse('portal_post_detail', args=['text', self.text_post.slug])
        response = self.client.get(url)
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        # Whitespace removal function credit - Cédric Julien
        # https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string
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
        url = reverse('portal_post_detail', args=['text_post', self.text_post.slug])
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'portal/text_post.html')

    def test_get_video_post_detail_page_with_active_subscriber(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.profile.subscription_status = 'active'
        user.profile.save()
        url = reverse('portal_post_detail',
                      args=['video_post', self.video_post.slug])
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'portal/video_post.html')

    def test_get_images_post_detail_page_with_active_subscriber(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.profile.subscription_status = 'active'
        user.profile.save()
        url = reverse('portal_post_detail',
                      args=['images_post', self.images_post.slug])
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'portal/images_post.html')

    # ADD PORTAL POSTS TESTS
    def test_user_must_be_staff_to_add_post(self):
        self.client.login(username='test_user', password='test_password')
        url = reverse('add_portal_post', args=['text_post'])
        response = self.client.get(url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'You must be a staff member add Portal posts.')
        self.assertEqual(response.status_code, 302)

    def test_add_valid_text_post_adds_post(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()
        url = reverse('add_portal_post', args=['text_post'])

        # Set up test_image
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        test_image = get_temporary_image(temp_file)
        test_image.seek(0)

        response = self.client.post(url, data={
            'title': 'Test Title',
            'post_blurb': 'Test blurb',
            'lead_image': test_image,
            'lead_image_summary': 'Test Summary',
            'text_content': 'Test content',
            'date_posted': '2021-08-26'
        })

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Text post added to Portal')
        # There should be 2 text posts, 1 created in setUp()
        self.assertEqual(len(PortalTextPost.objects.all()), 2)
        self.assertEqual(response.status_code, 302)

    def test_add_invalid_text_post_returns_correct_msssage_and_template(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()
        url = reverse('add_portal_post', args=['text_post'])

        response = self.client.post(url, data={
            'title': 'Test Title',
            'post_blurb': 'Test blurb',
            'slug': 'test-title',
            'lead_image': 'test_image',
            'lead_image_summary': 'Test Summary',
            'text_content': 'Test content',
            'date_posted': 'invalid datetime'
        })

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Error adding post, please try again.')
        # There should be 1 text post as 1 created in setUp()
        self.assertEqual(len(PortalTextPost.objects.all()), 1)
        self.assertEqual(response.status_code, 200)

    def test_add_valid_video_post_adds_post(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()
        url = reverse('add_portal_post', args=['video_post'])

        # Set up test_image
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        test_image = get_temporary_image(temp_file)
        test_image.seek(0)

        response = self.client.post(url, data={
            'title': 'Test Title',
            'post_blurb': 'Test blurb',
            'lead_image': test_image,
            'lead_image_summary': 'Test Summary',
            'video_url': 'http://www.test.com',
            'text_content': 'Test content',
            'date_posted': '2021-08-26'
        })

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Video post added to Portal')
        # There should be 2 text posts, 1 created in setUp()
        self.assertEqual(len(PortalVideoPost.objects.all()), 2)
        self.assertEqual(response.status_code, 302)

    def test_add_invalid_video_post_returns_correct_msssage_and_template(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()
        url = reverse('add_portal_post', args=['video_post'])

        response = self.client.post(url, data={
            'title': 'Test Title',
            'post_blurb': 'Test blurb',
            'slug': 'test-title',
            'lead_image': 'test_image',
            'lead_image_summary': 'Test Summary',
            'text_content': 'Test content',
            'date_posted': 'invalid datetime'
        })

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Error adding post, please try again.')
        # There should be 1 text post as 1 created in setUp()
        self.assertEqual(len(PortalVideoPost.objects.all()), 1)
        self.assertEqual(response.status_code, 200)

    def test_add_valid_images_post_adds_post(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()
        url = reverse('add_portal_post', args=['images_post'])

        # Set up test_images
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        lead_image = get_temporary_image(temp_file)
        lead_image.seek(0)

        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image_1 = get_temporary_image(temp_file)
        image_1.seek(0)

        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image_2 = get_temporary_image(temp_file)
        image_2.seek(0)

        response = self.client.post(url, data={
            'title': 'Test Title',
            'post_blurb': 'Test blurb',
            'lead_image': lead_image,
            'lead_image_summary': 'Test Summary',
            'image_1': image_1,
            'image_1_summary': 'Test Summary 1',
            'image_2': image_2,
            'image_2_summary': 'Test Summary 2',
            'video_url': 'http://www.test.com',
            'text_content': 'Test content',
            'date_posted': '2021-08-26'
        })

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Images post added to Portal')
        # There should be 2 text posts, 1 created in setUp()
        self.assertEqual(len(PortalImagesPost.objects.all()), 2)
        self.assertEqual(response.status_code, 302)

    def test_add_invalid_image_post_returns_correct_msssage_and_template(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()
        url = reverse('add_portal_post', args=['images_post'])

        response = self.client.post(url, data={
            'title': 'Test Title',
            'post_blurb': 'Test blurb',
            'lead_image': 'lead_image',
            'lead_image_summary': 'Test Summary',
            'image_1': 'image_1',
            'image_1_summary': 'Test Summary 1',
            'image_2': 'image_2',
            'image_2_summary': 'Test Summary 2',
            'video_url': 'http://www.test.com',
            'text_content': 'Test content',
            'date_posted': '2021-08-26'
        })

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Error adding post, please try again.')
        # There should be 1 text post as 1 created in setUp()
        self.assertEqual(len(PortalImagesPost.objects.all()), 1)
        self.assertEqual(response.status_code, 200)

    def test_get_add_text_post_returns_right_form_and_template(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()

        url = reverse('add_portal_post', args=['text_post'])
        response = self.client.get(url)
        form = response.context['form']

        self.assertEqual(str(form), 'AddTextPostForm')
        self.assertTemplateUsed('portal/add_text_post.html')

    def test_get_add_video_post_returns_right_form_and_template(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()

        url = reverse('add_portal_post', args=['video_post'])
        response = self.client.get(url)
        form = response.context['form']

        self.assertEqual(str(form), 'AddVideoPostForm')
        self.assertTemplateUsed('portal/add_video_post.html')

    def test_get_add_images_post_returns_right_form_and_template(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()

        url = reverse('add_portal_post', args=['images_post'])
        response = self.client.get(url)
        form = response.context['form']

        self.assertEqual(str(form), 'AddImagesPostForm')
        self.assertTemplateUsed('portal/add_images_post.html')

    # EDIT PORTAL POST TESTS
    def test_must_be_staff_to_edit_posts(self):
        self.client.login(username='test_user', password='test_password')
        url = reverse('edit_portal_post', args=['text_post', 1])
        response = self.client.get(url)
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'You must be a staff member to edit posts.')
        self.assertEqual(response.status_code, 302)

    def test_edit_text_post_edits_post(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()
        url = reverse('edit_portal_post', args=['text_post', 1])
        response = self.client.post(url, data={
            'title': 'updated text post',
            'post_blurb': 'Test blurb',
            'lead_image': 'test-image.jpg',
            'lead_image_summary': 'Test summary',
            'text_content': 'Test text content',
            'date_posted': '2021-08-26'
        })
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Post updated')

        updated_post = PortalTextPost.objects.get(pk=1)
        self.assertEqual(updated_post.title, 'updated text post')

    def test_edit_video_post_edits_post(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()
        url = reverse('edit_portal_post', args=['video_post', 1])
        response = self.client.post(url, data={
            'title': 'updated video post',
            'post_blurb': 'Test blurb',
            'lead_image': 'test-image.jpg',
            'lead_image_summary': 'Test summary',
            'video_url': 'http://www.test-url.com',
            'text_content': 'Test text content',
            'date_posted': '2021-08-26'
        })
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Post updated')

        updated_post = PortalVideoPost.objects.get(pk=1)
        self.assertEqual(updated_post.title, 'updated video post')

    def test_edit_images_post_edits_post(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()
        url = reverse('edit_portal_post', args=['images_post', 1])
        response = self.client.post(url, data={
            'title': 'updated images post',
            'post_blurb': 'Test blurb',
            'lead_image': 'test-image.jpg',
            'lead_image_summary': 'Test summary',
            'text_content': 'Test text content',
            'image_1': 'test-image.jpg',
            'image_1_summary': 'test summary',
            'image_2': 'test-image.jpg',
            'image_2_summary': 'test summary',
            'date_posted': '2021-08-26'
        })
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Post updated')

        updated_post = PortalImagesPost.objects.get(pk=1)
        self.assertEqual(updated_post.title, 'updated images post')

    def test_edit_with_bad_data_returns_message(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()
        url = reverse('edit_portal_post', args=['images_post', 1])
        response = self.client.post(url, data={
            'title': 'updated images post',
            'post_blurb': 'Test blurb',
            'lead_image': 'test-image.jpg',
            'lead_image_summary': 'Test summary',
            'text_content': 'Test text content',
            'image_1': 'test-image.jpg',
            'image_1_summary': 'test summary',
            'image_2': 'test-image.jpg',
            'image_2_summary': 'test summary',
            'date_posted': 'Invalid Datetime'
        })
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Error with form data, please check and try again.')

    def test_get_edit_text_post_returns_text_form(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()

        url = reverse('edit_portal_post', args=['text_post', 1])
        response = self.client.get(url)
        form = response.context['form']
        self.assertEqual(str(form), 'AddTextPostForm')

    def test_get_edit_video_post_returns_text_form(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()

        url = reverse('edit_portal_post', args=['video_post', 1])
        response = self.client.get(url)
        form = response.context['form']
        self.assertEqual(str(form), 'AddVideoPostForm')

    def test_get_images_video_post_returns_text_form(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()

        url = reverse('edit_portal_post', args=['images_post', 1])
        response = self.client.get(url)
        form = response.context['form']
        self.assertEqual(str(form), 'AddImagesPostForm')

    # DELETE PORTAL POSTS TESTS
    def test_must_be_staff_to_delete_posts(self):
        self.client.login(username='test_user', password='test_password')
        url = reverse('delete_portal_post', args=['text_post', 1])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        text_posts = PortalTextPost.objects.all()
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(text_posts), 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'You must be a staff member to delete posts.')

    def test_delete_text_post_deletes_post(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()
        url = reverse('delete_portal_post', args=['text_post', 1])
        response = self.client.get(url)
        text_posts = PortalTextPost.objects.all()
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Post Deleted.')
        self.assertEqual(len(text_posts), 0)
        self.assertEqual(response.status_code, 302)

    def test_delete_images_post_deletes_post(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()
        url = reverse('delete_portal_post', args=['images_post', 1])
        response = self.client.get(url)
        images_posts = PortalImagesPost.objects.all()
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Post Deleted.')
        self.assertEqual(len(images_posts), 0)
        self.assertEqual(response.status_code, 302)

    def test_delete_video_post_deletes_post(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.is_staff = True
        user.save()
        url = reverse('delete_portal_post', args=['video_post', 1])
        response = self.client.get(url)
        video_posts = PortalVideoPost.objects.all()
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Post Deleted.')
        self.assertEqual(len(video_posts), 0)
        self.assertEqual(response.status_code, 302)

    # PORTAL COMMENT TESTS
    def test_get_portal_text_post_comments(self):
        self.client.login(username='test_user_2', password='test_password')
        url = reverse('get_portal_comments')
        response = self.client.get(
            url,
            data={
                'object_id': self.text_post.id,
                'post_type': 'text_post',
                'page': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        # Get first element from the returned list as there will only
        # be one text post comment in the db
        response_json = response.json()[0]
        self.assertTrue('time' in response_json)
        self.assertTrue('posted_by' in response_json)
        self.assertTrue('id' in response_json)
        self.assertTrue('posted_by_img' in response_json)
        self.assertTrue('text' in response_json)
        self.assertTrue('has_prev' in response_json)
        self.assertTrue('has_next' in response_json)
        self.assertTrue('current_page' in response_json)
        self.assertFalse(response_json['edited'])
        self.assertFalse(response_json['comment_permissions'])

    def test_get_portal_video_post_comments(self):
        self.client.login(username='test_user_2', password='test_password')
        url = reverse('get_portal_comments')
        response = self.client.get(
            url,
            data={
                'object_id': self.video_post.id,
                'post_type': 'video_post',
                'page': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        # Get first element from the returned list as there will only
        # be one video post comment in the db
        response_json = response.json()[0]
        self.assertTrue('time' in response_json)
        self.assertTrue('posted_by' in response_json)
        self.assertTrue('id' in response_json)
        self.assertTrue('posted_by_img' in response_json)
        self.assertTrue('text' in response_json)
        self.assertTrue('has_prev' in response_json)
        self.assertTrue('has_next' in response_json)
        self.assertTrue('current_page' in response_json)
        self.assertFalse(response_json['edited'])
        self.assertFalse(response_json['comment_permissions'])

    def test_get_portal_images_post_comments(self):
        self.client.login(username='test_user_2', password='test_password')
        url = reverse('get_portal_comments')
        response = self.client.get(
            url,
            data={
                'object_id': self.images_post.id,
                'post_type': 'images_post',
                'page': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        # Get first element from the returned list as there will only
        # be one images post comment in the db
        response_json = response.json()[0]
        self.assertTrue('time' in response_json)
        self.assertTrue('posted_by' in response_json)
        self.assertTrue('id' in response_json)
        self.assertTrue('posted_by_img' in response_json)
        self.assertTrue('text' in response_json)
        self.assertTrue('has_prev' in response_json)
        self.assertTrue('has_next' in response_json)
        self.assertTrue('current_page' in response_json)
        self.assertFalse(response_json['edited'])
        self.assertFalse(response_json['comment_permissions'])

    def test_comment_permission_if_correct_user(self):
        self.client.login(username='test_user', password='test_password')
        url = reverse('get_portal_comments')
        response = self.client.get(
            url,
            data={
                'object_id': self.text_post.id,
                'page': 1,
                'post_type': 'text_post'
            }
        )

        response_json = response.json()[0]
        self.assertTrue(response_json['comment_permissions'])

    def test_must_have_portal_or_be_staff_to_add_comment(self):
        self.client.login(username='test_user', password='test_password')
        url = reverse('add_portal_comment')
        response = self.client.post(
            url,
            data={
                'user_id': self.test_user.id,
                'post_id': self.text_post.id,
                'comment': 'More test text',
                'post_type': 'text_post'
                }
            )
        messages = list(response.wsgi_request._messages)

        formatted_message = " ".join(str(messages[0]).split())
        expected_string = 'You must have an active subscription \
                           to add comments'
        formatted_expected_string = " ".join(expected_string.split())
        self.assertEqual(formatted_message, formatted_expected_string)
        self.assertEqual(response.status_code, 302)

    def test_add_portal_text_post_comment(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.profile.subscription_status = 'active'
        user.profile.save()
        url = reverse('add_portal_comment')
        response = self.client.post(
            url,
            data={
                'user_id': self.test_user.id,
                'post_id': self.text_post.id,
                'comment': 'More test text',
                'post_type': 'text_post'
                }
            )
        # Ensure comment has been saved to db
        # (Additional comment added in setUp())
        comment_count = len(TextPostComment.objects.all())
        self.assertEqual(comment_count, 2)
        self.assertEqual(response.status_code, 200)

    def test_add_portal_video_post_comment(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.profile.subscription_status = 'active'
        user.profile.save()
        url = reverse('add_portal_comment')
        response = self.client.post(
            url,
            data={
                'user_id': self.test_user.id,
                'post_id': self.video_post.id,
                'comment': 'More test text',
                'post_type': 'video_post'
                }
            )
        # Ensure comment has been saved to db
        # (Additional comment added in setUp())
        comment_count = len(VideoPostComment.objects.all())
        self.assertEqual(comment_count, 2)
        self.assertEqual(response.status_code, 200)

    def test_add_portal_images_post_comment(self):
        self.client.login(username='test_user', password='test_password')
        user = User.objects.get(username='test_user')
        user.profile.subscription_status = 'active'
        user.profile.save()
        url = reverse('add_portal_comment')
        response = self.client.post(
            url,
            data={
                'user_id': self.test_user.id,
                'post_id': self.images_post.id,
                'comment': 'More test text',
                'post_type': 'images_post',
                }
            )
        # Ensure comment has been saved to db
        # (Additional comment added in setUp())
        comment_count = len(ImagesPostComment.objects.all())
        self.assertEqual(comment_count, 2)
        self.assertEqual(response.status_code, 200)

    def test_edit_text_post_comment_(self):
        self.client.login(username='test_user', password='test_password')
        url = reverse('edit_portal_comment')
        response = self.client.post(
            url,
            data={
                'comment_id': self.text_post_comment.id,
                'edited_comment': 'This text is edited',
                'post_type': 'text_post'
                }
            )

        edited_comment = TextPostComment.objects.filter(
                id=self.text_post_comment.id).first()
        self.assertTrue(edited_comment.edited)
        self.assertEqual(edited_comment.text, 'This text is edited')
        self.assertEqual(response.status_code, 200)

    def test_edit_video_post_comment_(self):
        self.client.login(username='test_user', password='test_password')
        url = reverse('edit_portal_comment')
        response = self.client.post(
            url,
            data={
                'comment_id': self.video_post_comment.id,
                'edited_comment': 'This text is edited',
                'post_type': 'video_post'
                }
            )
        edited_comment = VideoPostComment.objects.filter(
                id=self.video_post_comment.id).first()
        self.assertTrue(edited_comment.edited)
        self.assertEqual(edited_comment.text, 'This text is edited')
        self.assertEqual(response.status_code, 200)

    def test_edit_images_post_comment_(self):
        self.client.login(username='test_user', password='test_password')
        url = reverse('edit_portal_comment')
        response = self.client.post(
            url,
            data={
                'comment_id': self.images_post_comment.id,
                'edited_comment': 'This text is edited',
                'post_type': 'images_post'
                }
            )
        edited_comment = ImagesPostComment.objects.filter(
                id=self.images_post_comment.id).first()
        self.assertTrue(edited_comment.edited)
        self.assertEqual(edited_comment.text, 'This text is edited')
        self.assertEqual(response.status_code, 200)

    def test_wrong_user_cant_edit_comment(self):
        self.client.login(
            username='test_user_2',
            password='test_password'
            )

        url = reverse('edit_portal_comment')
        response = self.client.post(
            url,
            data={
                'comment_id': self.text_post_comment.id,
                'edited_comment': 'This text is edited',
                'post_type': 'text_post'
                }
            )
        comment = TextPostComment.objects.filter(
                id=self.text_post_comment.id).first()
        self.assertEqual(comment.text, 'Test Text')
        self.assertEqual(response.status_code, 403)

    def test_delete_text_post_comment(self):
        self.client.login(
            username='test_user',
            password='test_password'
            )

        url = reverse('delete_portal_comment')
        response = self.client.post(
            url,
            data={
                'comment_id': self.text_post_comment.id,
                'post_type': 'text_post'
                }
            )
        comments = TextPostComment.objects.all()
        self.assertEqual(len(comments), 0)
        self.assertEqual(response.status_code, 200)

    def test_delete_video_post_comment(self):
        self.client.login(
            username='test_user',
            password='test_password'
            )

        url = reverse('delete_portal_comment')
        response = self.client.post(
            url,
            data={
                'comment_id': self.video_post_comment.id,
                'post_type': 'video_post'
                }
            )
        comments = VideoPostComment.objects.all()
        self.assertEqual(len(comments), 0)
        self.assertEqual(response.status_code, 200)

    def test_delete_images_post_comment(self):
        self.client.login(
            username='test_user',
            password='test_password'
            )

        url = reverse('delete_portal_comment')
        response = self.client.post(
            url,
            data={
                'comment_id': self.images_post_comment.id,
                'post_type': 'images_post'
                }
            )
        comments = ImagesPostComment.objects.all()
        self.assertEqual(len(comments), 0)
        self.assertEqual(response.status_code, 200)

    def test_wrong_user_cant_delete_comment(self):
        self.client.login(
            username='test_user_2',
            password='test_password'
            )

        url = reverse('delete_portal_comment')
        response = self.client.post(
            url,
            data={
                'comment_id': self.text_post_comment.id,
                'post_type': 'text_post',
                }
            )
        comments = TextPostComment.objects.all()
        self.assertEqual(len(comments), 1)
        self.assertEqual(response.status_code, 403)
