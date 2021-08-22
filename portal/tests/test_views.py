import json
from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from ..models import (PortalTextPost, PortalImagesPost, PortalVideoPost,
                      TextPostComment, VideoPostComment, ImagesPostComment)
from profiles.models import Profile


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

    # def test_get_portal_content_without_subscription_redirects(self):
    #     self.client.login(username='test_user', password='test_password')
    #     url = reverse('portal_content')
    #     response = self.client.get(url)
    #     messages = list(response.wsgi_request._messages)

    #     self.assertEqual(len(messages), 1)
    #     # Credit to Cédric Julien on Stack Overflow for this function to
    #     # remove whitepace from a string and add spaces
    #     # https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string
    #     formatted_message = " ".join(str(messages[0]).split())
    #     expected_string = 'Sorry, you must have an active subscription to \
    #         Portal to view this page.'
    #     formatted_expected_string = " ".join(expected_string.split())
    #     self.assertEqual(formatted_message, formatted_expected_string)
    #     self.assertRedirects(response, reverse('portal_info'))

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

    def test_get_portal_text_post_comments(self):
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
        # comment = Comment.objects.all().first()
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
