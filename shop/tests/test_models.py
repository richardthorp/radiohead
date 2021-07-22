from django.test import TestCase
from ..models import Album, Product


class TestShopModels(TestCase):
    def setUp(self):
        test_album = {
            "title": 'test_album',
            "year": 2021,
            "cd_price": 9.99,
            "vinyl_price": 19.99,
            "spotify_url": 'www.testurl.com',
            "tracklist": {"test": "test"},
            "image": 'media_files/album_covers/kid_a_cover.jpg'
            }
        self.album = Album.objects.create(**test_album)

        test_product = {
            "name": 'test_item',
            "category": 'clothing',
            "price": 9.99,
            "image": 'test_image.jpg'
        }
        self.product = Product.objects.create(**test_product)

    def test_album_str_method(self):
        self.assertEqual(str(self.album), 'test_album')

    def test_product_str_method(self):
        self.assertEqual(str(self.product), 'test_item')
