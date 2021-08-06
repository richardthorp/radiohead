from os import unlink
from PIL import Image
import tempfile
from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from shop.models import Album
from ..models import Single, Comment


def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGB", size, color)
    image.save(temp_file, 'jpeg')
    return temp_file


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

        self.staff_user = User.objects.create_user(
            username='staff_user',
            email='staff_user@email.com',
            password='test_password',
            is_staff=True,
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
        url = reverse('album_singles', args=[self.album.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media_app/album_singles.html')

    def test_get_single_content_page(self):
        url = reverse('single_content',
                      args=[self.album.slug, self.single.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media_app/single_content.html')

    def test_get_add_single__page(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        response = self.client.get('/media/add_single')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media_app/add_single.html')

    def test_must_be_staff_to_add_single(self):
        url = reverse('add_single')
        response = self.client.get(url)

        self.assertRedirects(response,
                             f"{reverse('account_login')}"
                             f"?next=/media/add_single")

    def test_add_single_view_adds_single_and_redirects(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        # Set up test_image
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        test_image = get_temporary_image(temp_file)
        test_image.seek(0)
        album = Album.objects.first()

        form_data = {
            "title": 'Another_test_single',
            "image": test_image,
            "album": album.id,
            'video_url': 'http://www.testurl.com',
            "spotify_url": 'http://www.testurl.com',
            }
        url = reverse('add_single')
        response = self.client.post(url, data=form_data)
        singles = Single.objects.all()
        added_single = Single.objects.get(title='Another_test_single')

        self.assertEqual(response.status_code, 302)
        # Expect 2 singles in db - 1 is created in setUp()
        self.assertEqual(len(singles), 2)
        self.assertRedirects(response,
                             reverse('album_singles',
                                     args=[added_single.album.slug]))

        # Remove the test_image from the file system
        unlink(added_single.image.path)

    def test_invalid_add_single_form_returns_message(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        form_data = {
            "title": '',
            "image": '',
            "album": '',
            'video_url': '',
            "spotify_url": '',
            }
        url = reverse('add_single')
        response = self.client.post(url, data=form_data)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Error adding single, please check form data')

    def test_get_edit_single_page(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        url = reverse('edit_single', args=[self.single.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media_app/edit_single.html')

    def test_must_be_staff_to_edit_single(self):
        self.client.login(
            username='test_user_1',
            password='test_password'
            )
        url = reverse('edit_single', args=[self.single.id])
        response = self.client.get(url)

        self.assertRedirects(response,
                             "/admin/login/?next=/media/edit_single/1")

    def test_edit_single_view_updates_single(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        # Set up test_image
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        test_image = get_temporary_image(temp_file)
        test_image.seek(0)

        form_data = {
            "title": 'Updated_single',
            "album": self.album.id,
            "spotify_url": 'http://www.testurl.com',
            "video_url": 'http://www.testurl.com',
            "image": test_image,
        }
        single = Single.objects.first()
        url = reverse('edit_single', args=[single.slug])
        response = self.client.post(url, data=form_data)
        messages = list(response.wsgi_request._messages)
        updated_single = Single.objects.first()

        self.assertEqual(updated_single.title, 'Updated_single')
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         f'{str(updated_single)} updated!')
        self.assertRedirects(response,
                             reverse('album_singles',
                                     args=[updated_single.album.slug]))
        # Remove the test_image from the file system
        unlink(updated_single.image.path)

    def test_edit_single_error_message_with_bad_data(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )

        form_data = {
            "title": '',
            "album": self.album.slug,
            "spotify_url": 'bad url',
            "video_url": 'www.testurl.com',
            "image": "test_image",
        }
        url = reverse('edit_single', args=[self.single.slug])
        response = self.client.post(url, data=form_data)
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Error with form data, please try again!')

    def test_delete_single(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        url = reverse('delete_single', args=[self.single.slug])
        response = self.client.get(url)
        messages = list(response.wsgi_request._messages)
        singles = Single.objects.all()
        self.assertEqual(len(singles), 0)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Single deleted.')

    def test_must_be_staff_to_delete_single(self):
        self.client.login(
            username='test_user_1',
            password='test_password'
            )
        url = reverse('delete_single', args=[self.single.slug])
        response = self.client.get(url)
        singles = Single.objects.all()
        self.assertEquals(len(singles), 1)
        self.assertRedirects(response,
                             f"/admin/login/?next=/media/delete_single/"
                             f"{self.single.slug}")

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
