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

    # ADD TO BAG VIEW TESTS
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
        expected_bag = {
            album.title: {
                'type': 'album',
                'items_by_format': {
                    'cd': 1
                }
            }
        }

        self.assertEqual(bag, expected_bag)
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
        expected_bag = {
            product.name: {
                'type': 'sized',
                'items_by_size': {
                    'M': 1
                }
            }
        }

        self.assertEqual(bag, expected_bag)
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

        expected_bag = {
            album.title: {
                'type': 'album',
                'items_by_format': {
                    'cd': 2
                }
            }
        }

        self.assertEqual(bag, expected_bag)

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

        expected_bag = {
            album.title: {
                'type': 'album',
                'items_by_format': {
                    'cd': 1,
                    'vinyl': 1
                }
            }
        }

        self.assertEqual(bag, expected_bag)

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

        expected_bag = {
            product.name: {
                'type': 'sized',
                'items_by_size': {
                    'M': 2
                }
            }
        }

        self.assertEqual(bag, expected_bag)

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

        expected_bag = {
            product.name: {
                'type': 'sized',
                'items_by_size': {
                    'M': 1,
                    'L': 1
                }
            }
        }

        self.assertEqual(bag, expected_bag)

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

        expected_bag = {
            product.name: 2
        }

        bag = self.client.session['bag']

        self.assertEqual(bag, expected_bag)

    def test_add_to_bag_get_request_redirects(self):
        product = Product.objects.get(name='test_other_item')
        url = reverse('add_to_bag', args=[product.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    # UPDATE BAG VIEW TESTS
    def test_update_item_to_less_than_one(self):
        product = Product.objects.first()
        url = reverse('update_bag', args=['product', product.id])
        data = {
            'quantity': 0
        }

        response = self.client.post(url, data=data)
        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'Click on the remove button to remove item from bag.')
        self.assertRedirects(response, reverse('view_bag'))

    def test_update_album_quantity_in_bag(self):
        album = Album.objects.first()
        # First, add items to the bag
        add_to_bag_url = reverse('add_to_bag', args=[album.id])
        add_to_bag_data = {
            'format': 'cd',
            'quantity': 2,
        }
        self.client.post(add_to_bag_url, data=add_to_bag_data)
        bag = self.client.session['bag']
        expected_initial_bag = {
            album.title: {
                'type': 'album',
                'items_by_format': {
                    'cd': 2
                }
            }
        }
        # Ensure 2 albums have been added to bag
        self.assertEqual(bag, expected_initial_bag)

        # Update album quantity to 5
        update_bag_url = reverse('update_bag', args=['cd', album.id])
        response = self.client.post(update_bag_url, data={'quantity': 5})
        bag = self.client.session['bag']
        messages = list(response.wsgi_request._messages)

        expected_bag = {
            album.title: {
                'type': 'album',
                'items_by_format': {
                    'cd': 5
                }
            }
        }
        # There should be 2 messages as one would be created in the call to
        # add_to_bag function above
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]),
                         'Item successfully updated in your bag.')
        self.assertEqual(bag, expected_bag)
        self.assertRedirects(response, reverse('view_bag'))

    def test_update_sized_product_quantity_in_bag(self):
        product = Product.objects.get(name='test_clothing_item')
        # First, add items to the bag
        add_to_bag_url = reverse('add_to_bag', args=[product.id])
        add_to_bag_data = {
            'size': 'M',
            'quantity': 2,
        }
        self.client.post(add_to_bag_url, data=add_to_bag_data)
        # Ensure 2 items have been added to bag
        bag = self.client.session['bag']
        expected_initial_bag = {
            product.name: {
                'type': 'sized',
                'items_by_size': {
                    'M': 2
                }
            }
        }
        self.assertEqual(bag, expected_initial_bag)

        # Update product quantity to 5
        update_bag_url = reverse('update_bag', args=['M', product.id])
        response = self.client.post(update_bag_url, data={'quantity': 5})
        bag = self.client.session['bag']
        messages = list(response.wsgi_request._messages)

        expected_bag = {
            product.name: {
                'type': 'sized',
                'items_by_size': {
                    'M': 5
                }
            }
        }

        # There should be 2 messages as one would be created in the call to
        # add_to_bag function above
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]),
                         'Item successfully updated in your bag.')
        self.assertEqual(bag, expected_bag)
        self.assertRedirects(response, reverse('view_bag'))

    def test_update_nonsized_product_quantity_in_bag(self):
        product = Product.objects.get(name='test_other_item')
        # First, add items to the bag
        add_to_bag_url = reverse('add_to_bag', args=[product.id])
        add_to_bag_data = {
            'quantity': 2
        }
        self.client.post(add_to_bag_url, data=add_to_bag_data)
        # Ensure 2 items have been added to bag
        bag = self.client.session['bag']
        self.assertEqual(bag, {product.name: 2})

        # Update product quantity to 5
        update_bag_url = reverse('update_bag', args=['other', product.id])
        response = self.client.post(update_bag_url, data={'quantity': 5})
        bag = self.client.session['bag']
        messages = list(response.wsgi_request._messages)

        # There should be 2 messages as one would be created in the call to
        # add_to_bag function above
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]),
                         'Item successfully updated in your bag.')
        self.assertEqual(bag, {product.name: 5})
        self.assertRedirects(response, reverse('view_bag'))

    def test_update_bag_get_request_redirects(self):
        product = Product.objects.get(name='test_other_item')
        url = reverse('update_bag', args=['other', product.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    # REMOVE ITEM FROM BAG VIEW TESTS
    def test_remove_album_from_bag(self):
        album = Album.objects.first()
        # First, add items to the bag
        add_to_bag_url = reverse('add_to_bag', args=[album.id])
        add_to_bag_data = {
            'format': 'cd',
            'quantity': 2,
        }
        self.client.post(add_to_bag_url, data=add_to_bag_data)
        bag = self.client.session['bag']
        expected_initial_bag = {
            'test_album': {
                'type': 'album',
                'items_by_format': {
                    'cd': 2
                }
            }
        }
        # Ensure 2 albums have been added to bag
        self.assertEqual(bag, expected_initial_bag)

        remove_item_url = reverse('remove_item', args=['cd', album.id])
        response = self.client.get(remove_item_url)
        bag = self.client.session['bag']
        messages = list(response.wsgi_request._messages)

        # There should be 2 messages as one would be created in the call to
        # add_to_bag function above
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]),
                         'Item successfully removed from your bag.')
        self.assertEqual(bag, {})
        self.assertEqual(response.status_code, 302)

    def test_remove_sized_product_from_bag(self):
        product = Product.objects.get(name='test_clothing_item')
        # First, add items to the bag
        add_to_bag_url = reverse('add_to_bag', args=[product.id])
        add_to_bag_data = {
            'size': 'M',
            'quantity': 2,
        }
        self.client.post(add_to_bag_url, data=add_to_bag_data)
        # Ensure 2 items have been added to bag
        bag = self.client.session['bag']
        expected_initial_bag = {
            product.name: {
                'type': 'sized',
                'items_by_size': {
                    'M': 2
                }
            }
        }
        self.assertEqual(bag, expected_initial_bag)

        remove_item_url = reverse('remove_item', args=['M', product.id])
        response = self.client.get(remove_item_url)
        bag = self.client.session['bag']
        messages = list(response.wsgi_request._messages)

        # There should be 2 messages as one would be created in the call to
        # add_to_bag function above
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]),
                         'Item successfully removed from your bag.')
        self.assertEqual(bag, {})
        self.assertEqual(response.status_code, 302)

    def test_remove_nonsized_product_from_bag(self):
        product = Product.objects.get(name='test_other_item')
        # First, add items to the bag
        add_to_bag_url = reverse('add_to_bag', args=[product.id])
        add_to_bag_data = {
            'quantity': 2,
        }
        self.client.post(add_to_bag_url, data=add_to_bag_data)
        # Ensure 2 items have been added to bag
        bag = self.client.session['bag']
        self.assertEqual(bag, {product.name: 2})

        remove_item_url = reverse('remove_item', args=['other', product.id])
        response = self.client.get(remove_item_url)
        bag = self.client.session['bag']
        messages = list(response.wsgi_request._messages)

        # There should be 2 messages as one would be created in the call to
        # add_to_bag function above
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]),
                         'Item successfully removed from your bag.')
        self.assertEqual(bag, {})
        self.assertEqual(response.status_code, 302)

    def test_remove_item_removes_correct_item(self):
        # First, add 'other' item to the bag
        other_product = Product.objects.get(name='test_other_item')
        add_to_bag_url = reverse('add_to_bag', args=[other_product.id])
        other_item_data = {
            'quantity': 1,
        }
        self.client.post(add_to_bag_url, data=other_item_data)

        # Then add 'sized' item to the bag
        sized_product = Product.objects.get(name='test_clothing_item')
        add_to_bag_url = reverse('add_to_bag', args=[sized_product.id])
        sized_item_data = {
            'size': 'M',
            'quantity': 1,
        }
        self.client.post(add_to_bag_url, data=sized_item_data)

        # Then add 'album' item to the bag
        album = Album.objects.first()
        # First, add items to the bag
        add_to_bag_url = reverse('add_to_bag', args=[album.id])
        album_data = {
            'format': 'cd',
            'quantity': 1,
        }
        self.client.post(add_to_bag_url, data=album_data)

        # Ensure 3 items have been added to bag
        bag = self.client.session['bag']
        self.assertEqual(len(bag), 3)

        # Just remove the 'other' item from the bag
        remove_item_url = reverse('remove_item',
                                  args=['other', other_product.id])
        response = self.client.get(remove_item_url)
        bag = self.client.session['bag']
        messages = list(response.wsgi_request._messages)

        # There should be 4 messages as 3 are created in the calls to
        # add_to_bag function above
        self.assertEqual(len(messages), 4)
        self.assertEqual(str(messages[3]),
                         'Item successfully removed from your bag.')
        expected_bag = {
            sized_product.name: {
                'type': 'sized',
                'items_by_size': {
                    'M': 1
                }
            },
            album.title: {
                'type': 'album',
                'items_by_format': {
                    'cd': 1
                }
            }
        }
        self.assertEqual(bag, expected_bag)
        self.assertEqual(response.status_code, 302)
