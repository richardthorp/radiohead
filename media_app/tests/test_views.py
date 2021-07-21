from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from shop.models import Album
from ..models import Single, Comment


class TestMediaViews(TestCase):

    def setUp(self):
        test_album = {"title": 'test_album',
                      "year": 2021,
                      "cd_price": 9.99,
                      "vinyl_price": 19.99,
                      "spotify_url": 'www.testurl.com',
                      "tracklist": {"test": "test"},
                      "image": 'media_files/album_covers/kid_a_cover.jpg'
                      }

        self.album = Album.objects.create(**test_album)

        test_single = {"title": 'test_single',
                       "album": self.album,
                       "spotify_url": 'www.testurl.com',
                       "video_url": 'www.testurl.com',
                       "image": 'media_files/single_covers/just_cover.jpg'
                       }

        self.single = Single.objects.create(**test_single)

        self.test_user_1 = User.objects.create_user(
            username='test_user_1',
            email='test_user_1@email.com',
            password='test_password'
            )

        self.test_user_2 = User.objects.create_user(
            username='test_user_2',
            email='test_user_2@email.com',
            password='test_password'
            )

        self.comment = Comment.objects.create(
            text='Test text',
            posted_by=self.test_user_1.profile,
            on_single=self.single,
            )

    def test_get_media_page(self):
        response = self.client.get('/media/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media_app/media.html')

    def test_get_album_singles_page(self):
        response = self.client.get(f'/media/album_singles/{self.album.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media_app/album_singles.html')

    def test_get_single_content_page(self):
        response = self.client.get(f'/media/single_content/{self.single.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media_app/single_content.html')

    def test_get_comments(self):
        url = reverse('get_comments')
        response = self.client.get(
            url,
            data={
                'objectID': self.single.id,
                'page': 1
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_get_comments_response_data(self):
        url = reverse('get_comments')
        response = self.client.get(
            url,
            data={
                'objectID': self.single.id,
                'page': 1
            }
        )
        # Get first element from the returned list as there will only
        # be one comment in the db
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
        self.client.login(
            username='test_user_1',
            password='test_password'
            )

        url = reverse('get_comments')
        response = self.client.get(
            url,
            data={
                'objectID': self.single.id,
                'page': 1
            }
        )

        response_json = response.json()[0]
        self.assertTrue(response_json['comment_permissions'])

    def test_add_comment(self):
        url = reverse('add_comment')
        response = self.client.post(
            url,
            data={
                'user_id': self.test_user_1.id,
                'object_id': self.single.id,
                'comment': 'More test text',
                }
            )
        # Ensure comment has been saved to db
        # (Additional comment added in setUp())
        comment_count = len(Comment.objects.all())
        self.assertEqual(comment_count, 2)
        self.assertEqual(response.status_code, 200)

    def test_edit_comment_(self):
        self.client.login(
            username='test_user_1',
            password='test_password'
            )

        url = reverse('edit_comment')
        response = self.client.post(
            url,
            data={
                'comment_id': self.comment.id,
                'edited_comment': 'This text is edited',
                }
            )

        edited_comment = Comment.objects.all().first()
        self.assertTrue(edited_comment.edited)
        self.assertEqual(edited_comment.text, 'This text is edited')
        self.assertEqual(response.status_code, 200)

    def test_wrong_user_cant_edit_comment(self):
        self.client.login(
            username='test_user_2',
            password='test_password'
            )

        url = reverse('edit_comment')
        response = self.client.post(
            url,
            data={
                'comment_id': self.comment.id,
                'edited_comment': 'This text is edited',
                }
            )

        comment = Comment.objects.all().first()
        self.assertEqual(comment.text, 'Test text')
        self.assertEqual(response.status_code, 403)

    def test_delete_comment(self):
        self.client.login(
            username='test_user_1',
            password='test_password'
            )

        url = reverse('delete_comment')
        response = self.client.post(
            url,
            data={
                'comment_id': self.comment.id,
                }
            )

        comments = Comment.objects.all()
        self.assertEqual(len(comments), 0)
        self.assertEqual(response.status_code, 200)

    def test_wrong_user_cant_delete_comment(self):
        self.client.login(
            username='test_user_2',
            password='test_password'
            )

        url = reverse('delete_comment')
        response = self.client.post(
            url,
            data={
                'comment_id': self.comment.id,
                }
            )
        comments = Comment.objects.all()
        self.assertEqual(len(comments), 1)
        self.assertEqual(response.status_code, 403)

# coverage run --source /workspace/radiohead manage.py test
