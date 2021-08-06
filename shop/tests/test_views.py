import json
from os import unlink
from PIL import Image
import tempfile
from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth.models import User
from ..models import Album, Product


def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGB", size, color)
    image.save(temp_file, 'jpeg')
    return temp_file


class TestShopViews(TestCase):
    def setUp(self):
        self.client = Client()
        temp_file = tempfile.NamedTemporaryFile()
        test_image = get_temporary_image(temp_file)
        test_image.seek(0)
        self.image = test_image.name
        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@email.com',
            password='test_password'
        )
        self.user_2 = User.objects.create_user(
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
        self.album = Album.objects.create(
            title='test_album',
            year=2021,
            cd_price=9.99,
            vinyl_price=19.99,
            spotify_url='www.testurl.com',
            tracklist={"test": "test"},
            image=self.image
        )
        self.album_str_tracklist = Album.objects.create(
            title='album_str_tracklist',
            year=2021,
            cd_price=9.99,
            vinyl_price=19.99,
            spotify_url='www.testurl.com',
            tracklist=json.dumps({"test": "test"}),
            image=self.image
        )
        self.clothing_product = Product.objects.create(
            name='test_clothing_item',
            category='clothing',
            price=9.99,
            image=self.image
        )
        self.other_product = Product.objects.create(
            name='test_other_item',
            category='other',
            price=9.99,
            image=self.image
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
        url = reverse('shop_detail', args=['album', self.album.slug])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('shop/album.html')

    # Product template
    def test_shop_detail_view_with_product(self):
        url = reverse(
            'shop_detail', args=['product', self.clothing_product.slug]
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
        # Set up test_image
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        test_image = get_temporary_image(temp_file)
        test_image.seek(0)

        form_data = {
            "name": 'test_add_clothing_item',
            "category": 'clothing',
            "price": 9.99,
            'description': "testing",
            "image": test_image,
        }
        url = reverse('add_product', args=['product'])
        response = self.client.post(url, data=form_data)

        added_product = Product.objects.get(name='test_add_clothing_item')
        products = Product.objects.all()

        self.assertEqual(response.status_code, 302)
        # Expect 3 products in db - 2 are created in setUp()
        # product_count = len(Product.objects.all())
        self.assertEqual(len(products), 3)
        self.assertRedirects(response,
                             reverse('shop_detail',
                                     args=['product', added_product.slug]))
        # Remove the test_image from the file system
        unlink(added_product.image.path)

    # Test adding an album
    def test_add_product_view_adds_album_and_redirects(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        # Set up test_image
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        test_image = get_temporary_image(temp_file)
        test_image.seek(0)

        form_data = {
            "title": 'test_add_album',
            "year": 2021,
            "cd_price": 9.99,
            "vinyl_price": 19.99,
            "spotify_url": 'www.testurl.com',
            "tracklist": json.dumps({"test": "test"}),
            "image": test_image,
            }
        url = reverse('add_product', args=['album'])
        response = self.client.post(url, data=form_data)

        albums = Album.objects.all()
        added_album = Album.objects.get(title='test_add_album')

        self.assertEqual(response.status_code, 302)
        # Expect 3 albums in db as 2 is created in setUp()
        self.assertEqual(len(albums), 3)
        self.assertRedirects(response,
                             reverse('shop_detail',
                                     args=['album', added_album.slug]))

        # Remove the test_image from the file system
        unlink(added_album.image.path)

    def test_add_product_error_message_with_bad_data(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        form_data = {
            "name": '',
            "category": '',
            "price": 9.99,
            'description': "testing",
            "image": 'test_image',
        }
        url = reverse('add_product', args=['product'])
        response = self.client.post(url, data=form_data)
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Error adding product, please try again.')

    # Edit product tests
    def test_get_edit_product_page_for_album(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        url = reverse('edit_product', args=['album', self.album.slug])
        response = self.client.get(url)

        self.assertEqual(str(response.context['form']), 'AddAlbumForm')
        self.assertTemplateUsed('shop/edit_product.html')
        self.assertEqual(response.status_code, 200)

    def test_get_edit_product_page_for_album_with_str_tracklist(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        url = reverse('edit_product',
                      args=['album', self.album_str_tracklist.id])
        response = self.client.get(url)

        self.assertEqual(str(response.context['form']), 'AddAlbumForm')
        self.assertTemplateUsed('shop/edit_product.html')
        self.assertEqual(response.status_code, 200)

    def test_get_edit_product_page_for_product(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        url = reverse('edit_product', args=['product', self.other_product.slug])
        response = self.client.get(url)

        self.assertEqual(str(response.context['form']), 'AddProductForm')
        self.assertTemplateUsed('shop/edit_product.html')
        self.assertEqual(response.status_code, 200)

    def test_must_be_staff_to_edit_product(self):
        url = reverse('edit_product', args=['album', self.album.slug])
        response = self.client.get(url)

        self.assertRedirects(response,
                             f"{reverse('account_login')}"
                             f"?next=/shop/edit_product/album/1")

    def test_edit_product_view_updates_product(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        # Set up test_image
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        test_image = get_temporary_image(temp_file)
        test_image.seek(0)

        form_data = {
            'name': 'updated_other_item',
            'category': 'other',
            'price': 9.99,
            'description': "testing",
            'image': test_image,
        }
        url = reverse('edit_product',
                      args=['product', self.clothing_product.slug])
        response = self.client.post(url, data=form_data)
        messages = list(response.wsgi_request._messages)
        updated_product = Product.objects.get(slug=self.clothing.slug)

        self.assertEqual(updated_product.name, 'updated_other_item')
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Product updated!')
        self.assertRedirects(response,
                             reverse('shop_detail',
                                     args=['product', updated_product.slug]))
        # Remove the test_image from the file system
        unlink(updated_product.image.path)

    def test_edit_product_view_updates_album(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        # Set up test_image
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        test_image = get_temporary_image(temp_file)
        test_image.seek(0)

        form_data = {
            'title': 'updated_album',
            'year': 2021,
            'cd_price': 9.99,
            'vinyl_price': 19.99,
            'spotify_url': 'www.testurl.com',
            'tracklist': json.dumps("test: test"),
            'image': test_image,
        }
        url = reverse('edit_product',
                      args=['album', self.album.slug])
        response = self.client.post(url, data=form_data)
        messages = list(response.wsgi_request._messages)
        updated_product = Album.objects.get(slug=self.album.slug)

        self.assertEqual(updated_product.title, 'updated_album')
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Product updated!')
        self.assertRedirects(response,
                             reverse('shop_detail',
                                     args=['album', updated_product.slug]))
        # Remove the test_image from the file system
        unlink(updated_product.image.path)

    def test_edit_album_error_message_with_bad_data(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )

        form_data = {
            'title': '',
            'year': 2021,
            'cd_price': 9.99,
            'vinyl_price': 19.99,
            'spotify_url': 'www.testurl.com',
            'tracklist': json.dumps("test: test"),
            'image': 'test_image',
        }
        url = reverse('edit_product', args=['album', self.album.slug])
        response = self.client.post(url, data=form_data)
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Error with form data, please try again!')

    # Delete product tests
    def test_delete_album(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        url = reverse('delete_product', args=['album', self.album.slug])
        response = self.client.get(url)
        albums = Album.objects.all()

        # There should be 1 album left as 2 are created in setUp()
        self.assertEqual(len(albums), 1)
        self.assertRedirects(response, reverse('shop'))

    def test_delete_product(self):
        self.client.login(
            username='staff_user',
            password='test_password'
            )
        url = reverse('delete_product', args=['product', self.other_product.slug])
        response = self.client.get(url)
        products = Product.objects.all()

        self.assertEqual(len(products), 1)
        self.assertRedirects(response, reverse('shop'))

    def test_must_be_staff_to_delete_product(self):
        url = reverse('delete_product', args=['album', self.album.slug])
        response = self.client.get(url)

        self.assertRedirects(response,
                             f"{reverse('account_login')}"
                             f"?next=/shop/delete_product/album/1")
