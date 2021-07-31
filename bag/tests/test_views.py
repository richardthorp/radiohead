from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from shop.models import Product, Album


class TestBagViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@email.com',
            password='test_password'
        )
        self.album = Album.objects.create(
            title='test_album',
            year=2021,
            cd_price=9.99,
            vinyl_price=19.99,
            spotify_url='www.testurl.com',
            tracklist={"test": "test"},
            image='self.image'
        )
        self.clothing_product = Product.objects.create(
            name='test_clothing_item',
            category='clothing',
            price=9.99,
            image='self.image'
        )
        self.other_product = Product.objects.create(
            name='test_other_item',
            category='other',
            price=9.99,
            image='self.image'
        )

    def test_get_view_bag_page(self):
        url = reverse('view_bag')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('bag/view_bag.html')

    def test_add_album_to_bag_adds_to_session(self):
        album = Album.objects.first()
        url = reverse('add_to_bag', args=[album.id])
        data = {
            'format': 'cd',
            'quantity': 1,
        }
        self.client.post(url, data=data)
        bag = self.client.session['bag']
        expected_dict = {
            'test_album': {
                'type': 'album',
                'cd': 1
            }
        }
        self.assertEqual(bag, expected_dict)
        self.assertEqual(len(bag), 1)

    def test_add_sized_product_to_bag_adds_to_session(self):
        product = Product.objects.get(name='test_clothing_item')
        url = reverse('add_to_bag', args=[product.id])
        data = {
            'size': 'M',
            'quantity': 1,
        }
        self.client.post(url, data=data)
        bag = self.client.session['bag']
        expected_dict = {
            'test_clothing_item': {
                'type': 'sized',
                'M': 1
            }
        }
        self.assertEqual(bag, expected_dict)
        self.assertEqual(len(bag), 1)

    def test_product_quantity_must_be_more_than_one(self):
        product = Product.objects.first()
        url = reverse('add_to_bag', args=[product.id])
        data = {
            'size': 'M',
            'quantity': 0,
        }
        response = self.client.post(url, data=data)
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'You can not add less than one item to your bag!')
        self.assertNotIn('bag', self.client.session)
        self.assertRedirects(response, reverse('shop_detail',
                                               args=['product', product.id]))

    def test_album_quantity_must_be_more_than_one(self):
        album = Album.objects.first()
        url = reverse('add_to_bag', args=[album.id])
        data = {
            'format': 'cd',
            'quantity': 0,
        }
        album = Album.objects.get(pk=1)
        response = self.client.post(url, data=data)
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'You can not add less than one item to your bag!')
        self.assertNotIn('bag', self.client.session)
        self.assertRedirects(response, reverse('shop_detail',
                                               args=['album', album.id]))

    def test_add_same_album_and_format_twice(self):
        album = Album.objects.first()
        url = reverse('add_to_bag', args=[album.id])

        initial_add = {
            'format': 'cd',
            'quantity': 1,
        }
        self.client.post(url, data=initial_add)

        second_add = {
            'format': 'cd',
            'quantity': 1,
        }
        self.client.post(url, data=second_add)
        bag = self.client.session['bag']

        expected_dict = {
            album.title: {
                'type': 'album',
                'cd': 2
            }
        }
        self.assertEqual(bag, expected_dict)

    def test_add_same_album_different_format(self):
        album = Album.objects.first()
        url = reverse('add_to_bag', args=[album.id])

        initial_add = {
            'format': 'cd',
            'quantity': 1,
        }
        self.client.post(url, data=initial_add)

        second_add = {
            'format': 'vinyl',
            'quantity': 1,
        }
        self.client.post(url, data=second_add)

        bag = self.client.session['bag']

        expected_dict = {
            album.title: {
                'type': 'album',
                'cd': 1,
                'vinyl': 1
            }
        }
        self.assertEqual(bag, expected_dict)

    def test_add_same_product_and_size_twice(self):
        product = Product.objects.first()
        url = reverse('add_to_bag', args=[product.id])

        initial_add = {
            'size': 'M',
            'quantity': 1,
        }
        self.client.post(url, data=initial_add)

        second_add = {
            'size': 'M',
            'quantity': 1,
        }
        self.client.post(url, data=second_add)
        bag = self.client.session['bag']

        expected_dict = {
            product.name: {
                'type': 'sized',
                'M': 2
            }
        }
        self.assertEqual(bag, expected_dict)

    def test_add_same_product_different_size(self):
        product = Product.objects.first()
        url = reverse('add_to_bag', args=[product.id])

        initial_add = {
            'size': 'M',
            'quantity': 1,
        }
        self.client.post(url, data=initial_add)

        second_add = {
            'size': 'L',
            'quantity': 1,
        }
        self.client.post(url, data=second_add)

        bag = self.client.session['bag']

        expected_dict = {
            product.name: {
                'type': 'sized',
                'M': 1,
                'L': 1
            }
        }
        self.assertEqual(bag, expected_dict)

    def test_add_same_nonsized_product(self):
        product = Product.objects.get(name='test_other_item')
        url = reverse('add_to_bag', args=[product.id])
        initial_add = {
            'quantity': 1,
        }
        self.client.post(url, data=initial_add)

        second_add = {
            'quantity': 1
        }
        self.client.post(url, data=second_add)

        expected_dict = {
            product.name: 2
        }

        bag = self.client.session['bag']

        self.assertEqual(bag, expected_dict)

    def test_add_to_bag_get_request_redirects(self):
        product = Product.objects.get(name='test_other_item')
        url = reverse('add_to_bag', args=[product.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
