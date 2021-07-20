from django.test import TestCase
from shop.models import Album
from ..models import Single


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

    def test_get_media_page(self):
        response = self.client.get('/media/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media_app/media.html')

    def test_get_album_singles_page(self):
        response = self.client.get(f'/media/album_singles/{self.single.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'media_app/album_singles.html')
