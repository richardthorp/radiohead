from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Comment, Single
from shop.models import Album


class TestMediaAppModels(TestCase):
    def setUp(self):
        test_album = {"title": 'test_album',
                      "year": 2021,
                      "cd_price": 9.99,
                      "vinyl_price": 19.99,
                      "spotify_url": 'www.testurl.com',
                      "tracklist": {"test": "test"},
                      "image": 'test_image.jpg'
                      }

        self.album = Album.objects.create(**test_album)

        test_single = {"title": 'test_single',
                       "album": self.album,
                       "spotify_url": 'www.testurl.com',
                       "video_url": 'www.testurl.com',
                       "image": 'test_image.jpg'
                       }

        self.single = Single.objects.create(**test_single)

        self.test_user_1 = User.objects.create_user(
            username='test_user_1',
            email='test_user_1@email.com',
            password='test_password'
            )

        self.comment = Comment.objects.create(
            text='Test text',
            posted_by=self.test_user_1.profile,
            on_single=self.single,
            )

    def test_comment_str_method(self):
        self.assertEqual(
            str(self.comment),
            f""" Comment by {self.test_user_1}'s Profile on {self.comment.date_posted}.
            """
        )

    def test_single_str_method(self):
        self.assertEqual(
            str(self.single),
            'test_single'
        )
