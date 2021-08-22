from django.test import TestCase
from django.contrib.auth.models import User
from ..models import (PortalImagesPost, PortalTextPost, PortalVideoPost,
                      TextPostComment, VideoPostComment, ImagesPostComment)


class TestPortslModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@email.com',
            password='test_password'
        )
        self.portal_text_post = PortalTextPost.objects.create(
            title='Test Text Title',
            post_blurb='Test Blurb',
            slug='test-title',
            lead_image='image.jpg',
            lead_image_summary='image summary',
            text_content='text content'
        )
        self.portal_images_post = PortalImagesPost.objects.create(
            title='Test Images Title',
            post_blurb='Test Blurb',
            slug='test-title',
            lead_image='image.jpg',
            lead_image_summary='image summary',
            text_content='text content',
            image_1='image.jpg',
            image_1_summary='image_summary',
            image_2='image.jpg',
            image_2_summary='image summary'
            )
        self.portal_video_post = PortalVideoPost.objects.create(
            title='Test Video Title',
            post_blurb='Test Blurb',
            slug='test-title',
            lead_image='image.jpg',
            lead_image_summary='image summary',
            video_url='http://www.test.com',
            text_content='text content'
        )
        self.video_post_comment = VideoPostComment.objects.create(
            text='text',
            posted_by=self.user.profile,
            post=self.portal_video_post
        )
        self.text_post_comment = TextPostComment.objects.create(
            text='text',
            posted_by=self.user.profile,
            post=self.portal_text_post
        )
        self.images_post_comment = ImagesPostComment.objects.create(
            text='text',
            posted_by=self.user.profile,
            post=self.portal_images_post
        )

    def test_portal_text_post_str_method(self):
        self.assertEqual(str(self.portal_text_post),
                         "Text post: Test Text Title")

    def test_portal_images_post_str_method(self):
        self.assertEqual(str(self.portal_images_post),
                         "Images post: Test Images Title")

    def test_portal_video_post_str_method(self):
        self.assertEqual(str(self.portal_video_post),
                         "Video post: Test Video Title")

    def test_text_post_comment_str_method(self):
        self.assertEqual(
            str(self.text_post_comment),
            f"Comment by test_user's Profile on "
            f"{self.text_post_comment.date_posted}.")

    def test_video_post_comment_str_method(self):
        self.assertEqual(
            str(self.video_post_comment),
            f"Comment by test_user's Profile on "
            f"{self.video_post_comment.date_posted}.")

    def test_images_post_comment_str_method(self):
        self.assertEqual(
            str(self.images_post_comment),
            f"Comment by test_user's Profile on "
            f"{self.images_post_comment.date_posted}.")
