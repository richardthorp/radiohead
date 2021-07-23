from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
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

        self.test_user = User.objects.create_user(
            username='test_user',
            email='test_user@email.com',
            password='test_password',
        )

        self.staff_user = User.objects.create_user(
            username='staff_user',
            email='staff_user@email.com',
            password='test_password',
            is_staff=True,
        )

    # SHOP VIEW TESTS
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

    # SHOP DETAIL VIEW TESTS
    # Album template
    def test_shop_detail_view_with_album(self):
        url = reverse('shop_detail', args=['album', self.album.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('shop/album.html')

    # Product template
    def test_shop_detail_view_with_product(self):
        url = reverse(
            'shop_detail', args=['product', self.clothing_product.id]
            )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('shop/product.html')

    # PRODUCT MANAGEMENT VIEW TESTS
    # Add product tests
    def test_get_add_product_page(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        url = reverse('add_product', args=['album'])
        response = self.client.get(url)

        self.assertTemplateUsed('shop/add_product.html')
        self.assertEqual(response.status_code, 200)

    def test_must_be_staff_to_add_product(self):
        url = reverse('add_product', args=['album'])
        response = self.client.get(url)
        self.assertRedirects(response,
                             f"{reverse('account_login')}"
                             f"?next=/shop/add_product/album")

    def test_add_album_view_returns_correct_form(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        url = reverse('add_product', args=['album'])
        response = self.client.get(url)
        self.assertEqual(str(response.context['form']), 'AddAlbumForm')

    def test_add_product_view_returns_correct_form(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        url = reverse('add_product', args=['product'])
        response = self.client.get(url)
        self.assertEqual(str(response.context['form']), 'AddProductForm')

    # Test adding a product
    def test_add_product_view_adds_product_and_redirects(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )

        form_data = {
            "name": 'test_add_clothing_item',
            "category": 'clothing',
            "price": 9.99,
            'description': "testing",
            "image": 'test_image.jpg'
        }
        url = reverse('add_product', args=['product'])

        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)

        # Expect 3 products in db - 2 are created in setUp()
        product_count = len(Product.objects.all())
        self.assertEqual(product_count, 3)

        added_product = Product.objects.get(name='test_add_clothing_item')
        self.assertRedirects(response,
                             reverse('shop_detail',
                                     args=['product', added_product.id]))

        # Test adding an album
        def test_add_product_view_adds_album_and_redirects(self):
            self.client.login(
                username='staff_user',
                password='test_password'
                )

            form_data = {
                "title": 'test_add_album',
                "year": 2021,
                "cd_price": 9.99,
                "vinyl_price": 19.99,
                "spotify_url": 'www.testurl.com',
                "tracklist": {"test": "test"},
                "image": 'media_files/album_covers/kid_a_cover.jpg'
                }
            url = reverse('add_product', args=['album'])

            response = self.client.post(url, data=form_data)
            self.assertEqual(response.status_code, 302)

            # Expect 2 albums in db - 1 is created in setUp()
            product_count = len(Product.objects.all())
            self.assertEqual(product_count, 3)

            added_album = Album.objects.get(name='test_add_album')
            self.assertRedirects(response,
                                 reverse('shop_detail',
                                         args=['album', added_album.id]))

    # Edit product tests
    def test_get_edit_product_page(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        url = reverse('edit_product', args=['album', self.album.id])
        response = self.client.get(url)

        self.assertTemplateUsed('shop/edit_product.html')
        self.assertEqual(response.status_code, 200)

    def test_must_be_staff_to_edit_product(self):
        url = reverse('edit_product', args=['album', self.album.id])
        response = self.client.get(url)
        self.assertRedirects(response,
                             f"{reverse('account_login')}"
                             f"?next=/shop/edit_product/album/1")

    # Delete product tests
    def test_delete_product(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        url = reverse('delete_product', args=['album', self.album.id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('shop'))
        albums = Album.objects.all()
        self.assertEqual(len(albums), 0)

    def test_must_be_staff_to_delete_product(self):
        url = reverse('delete_product', args=['album', self.album.id])
        response = self.client.get(url)
        self.assertRedirects(response,
                             f"{reverse('account_login')}"
                             f"?next=/shop/delete_product/album/1")
