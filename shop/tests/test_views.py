from django.test import TestCase
from django.shortcuts import reverse
from ..models import Album, Product


class TestShopViews(TestCase):
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

        test_clothing_product = {
            "name": 'test_clothing_item',
            "category": 'clothing',
            "price": 9.99,
            "image": 'test_image.jpg'
        }
        self.clothing_product = Product.objects.create(**test_clothing_product)

        test_other_product = {
            "name": 'test_other_item',
            "category": 'other',
            "price": 9.99,
            "image": 'test_image.jpg'
        }
        self.other_product = Product.objects.create(**test_other_product)

    def test_get_shop_page(self):
        url = reverse('shop')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.context.keys())
        self.assertTemplateUsed(response, 'shop/shop.html')

    def test_filter_by_music(self):
        url = reverse('shop')
        response = self.client.post(
            url,
            data={'filter': 'music'}
            )

        self.assertIn(self.album, response.context['items'])
        self.assertNotIn(self.clothing_product, response.context['items'])
        self.assertNotIn(self.other_product, response.context['items'])

    def test_filter_by_clothing(self):
        url = reverse('shop')
        response = self.client.post(
            url,
            data={'filter': 'clothing'}
            )

        self.assertIn(self.clothing_product, response.context['items'])
        self.assertNotIn(self.album, response.context['items'])
        self.assertNotIn(self.other_product, response.context['items'])

    def test_filter_by_other(self):
        url = reverse('shop')
        response = self.client.post(
            url,
            data={'filter': 'other'}
            )

        self.assertIn(self.other_product, response.context['items'])
        self.assertNotIn(self.album, response.context['items'])
        self.assertNotIn(self.clothing_product, response.context['items'])

    def test_shop_detail_view_with_album(self):
        url = reverse('shop_detail', args=['album', self.album.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('shop/album.html')

    def test_shop_detail_view_with_product(self):
        url = reverse(
            'shop_detail', args=['product', self.clothing_product.id]
            )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('shop/product.html')
