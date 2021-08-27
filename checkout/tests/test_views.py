# from stripe.PaymentIntent import modify
from decimal import Decimal
from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from shop.models import Album, Product
from profiles.models import Profile
from profiles.forms import ProfileForm
from ..models import Order, AlbumOrderLineItem, ProductOrderLineItem
from ..forms import OrderForm


class TestCheckoutViews(TestCase):
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
            image='test_image'
        )
        self.clothing_product = Product.objects.create(
            name='test_clothing_item',
            category='clothing',
            price=9.99,
            image='test_image'
        )
        self.other_product = Product.objects.create(
            name='test_other_item',
            category='other',
            price=9.99,
            image='test_image'
        )
        self.order = Order.objects.create(
            email='test@email.com',
            name='Test User',
            phone_number='12345678901',
            address_line1='Test Line 1',
            town_or_city='Test Town',
            country='GB'
            )
        self.product_line_item = ProductOrderLineItem.objects.create(
            order=self.order,
            product=self.clothing_product,
            size='S',
            quantity=1
            )
        self.album_line_item = AlbumOrderLineItem.objects.create(
            order=self.order,
            album=self.album,
            format='cd',
            quantity=1
            )

    def test_get_checkout_page_with_empty_bag(self):
        url = reverse('checkout')
        response = self.client.get(url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Add items to your bag to checkout.")
        self.assertRedirects(response, reverse('shop'))

    def test_get_checkout_page_with_bag_item(self):
        # Add an item to session['bag']
        add_to_bag_url = reverse('add_to_bag', args=[self.album.slug])
        self.client.post(add_to_bag_url, data={
            'quantity': 1,
            'format': 'cd',
        })

        checkout_url = reverse('checkout')
        response = self.client.get(checkout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('checkout/checkout.html')

    def test_checkout_post_view_creates_order_and_redirects(self):
        self.client.login(
            username='test_user',
            password='test_password'
            )
        # Add an album to session['bag']
        add_to_bag_url = reverse('add_to_bag', args=[self.album.slug])
        self.client.post(add_to_bag_url, data={
            'quantity': 1,
            'format': 'cd',
        })
        # Add a sized product to session['bag']
        add_to_bag_url = reverse('add_to_bag',
                                 args=[self.clothing_product.slug])
        self.client.post(add_to_bag_url, data={
            'quantity': 1,
            'size': 'M',
        })
        # Add a non-sized product to session['bag']
        add_to_bag_url = reverse('add_to_bag',
                                 args=[self.other_product.slug])
        self.client.post(add_to_bag_url, data={
            'quantity': 1,
        })
        checkout_url = reverse('checkout')
        post_data = {
            'name': 'New Test User',
            'email': 'test@user.com',
            'phone_number': 12345678901,
            'address_line1': 'Test Line 1',
            'address_line2': 'Test Line 2',
            'town_or_city': 'Test Town',
            'county': 'Test County',
            'postcode': 'POSTCODE',
            'country': 'GB',
            'client_secret': 'test_client_secret',
            'save_details': 'true',
        }
        response = self.client.post(checkout_url, data=post_data)

        # Ensure an order has been created -
        # One already created in SetUp
        orders = Order.objects.all()
        self.assertEqual(len(orders), 2)

        # Check AlbumOrderLineItem has been created
        # One already created in SetUp
        album_line_items = AlbumOrderLineItem.objects.all()
        self.assertEqual(len(album_line_items), 2)

        # Check 3 ProductOrderLineItems have been created -
        # 1 created in SetUp and 2 created from bag in call to
        # checkout above
        product_line_items = ProductOrderLineItem.objects.all()
        self.assertEqual(len(product_line_items), 3)

        # Get the newly created order
        order = Order.objects.get(name='New Test User')

        self.assertRedirects(response,
                             reverse('checkout_success',
                                     args=[order.order_number]))

        # Ensure 'save_details' has been added to session
        self.assertIn('save_details', self.client.session)

    def test_anonymous_user_can_checkout(self):
        # Add an album to session['bag']
        add_to_bag_url = reverse('add_to_bag', args=[self.album.slug])
        self.client.post(add_to_bag_url, data={
            'quantity': 1,
            'format': 'cd',
        })
        checkout_url = reverse('checkout')
        post_data = {
            'name': 'Anonymous Test User',
            'email': 'test@user.com',
            'phone_number': 12345678901,
            'address_line1': 'Test Line 1',
            'address_line2': 'Test Line 2',
            'town_or_city': 'Test Town',
            'county': 'Test County',
            'postcode': 'POSTCODE',
            'country': 'GB',
            'client_secret': 'test_client_secret',
        }
        response = self.client.post(checkout_url, data=post_data)

        # Ensure an order has been created -
        # one already created in SetUp
        orders = Order.objects.all()
        self.assertEqual(len(orders), 2)

        # Ensure AlbumOrderLineItem has been created -
        # one already created in SetUp
        album_line_items = AlbumOrderLineItem.objects.all()
        self.assertEqual(len(album_line_items), 2)

        # Get the newly created order
        order = Order.objects.get(name='Anonymous Test User')
        self.assertRedirects(response,
                             reverse('checkout_success',
                                     args=[order.order_number]))

    def test_authenticated_user_gets_associated_profile_in_get_checkout(self):
        # Log in user with a profile
        self.client.login(
            username='test_user',
            password='test_password'
            )
        # Set the default fields on the profile
        profile_data = {
            'default_name': 'Test User',
            'default_email': 'user@test.com',
            'default_phone_number': '12345678901',
            'default_address_line1': 'Test Line 1',
            'default_address_line2': 'Test Line 2',
            'default_town_or_city': 'Test Town',
            'default_county': 'Test County',
            'default_postcode': 'POSTCODE',
            'default_country': 'GB',
        }
        form = ProfileForm(profile_data, instance=self.user.profile)
        form.save()

        # Add an item to session['bag']
        add_to_bag_url = reverse('add_to_bag', args=[self.album.slug])
        self.client.post(add_to_bag_url, data={
            'quantity': 1,
            'format': 'cd',
        })
        checkout_url = reverse('checkout')
        response = self.client.get(checkout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('checkout/checkout.html')
        # Compile initial form data into a dict to compare with profile
        # data saved to profile above
        initial_form_data = {}
        for field, value in response.context['form'].initial.items():
            # The country field will be formatted differently due to
            # django_countries processing the form data
            if field == 'country':
                initial_form_data['default_country'] = 'GB'
            else:
                initial_form_data[f"default_{field}"] = value

        self.assertEqual(profile_data['default_name'],
                         initial_form_data['default_name'])
        self.assertEqual(profile_data['default_phone_number'],
                         initial_form_data['default_phone_number'])
        self.assertEqual(profile_data['default_address_line1'],
                         initial_form_data['default_address_line1'])
        self.assertEqual(profile_data['default_address_line2'],
                         initial_form_data['default_address_line2'])
        self.assertEqual(profile_data['default_town_or_city'],
                         initial_form_data['default_town_or_city'])
        self.assertEqual(profile_data['default_county'],
                         initial_form_data['default_county'])
        self.assertEqual(profile_data['default_postcode'],
                         initial_form_data['default_postcode'])
        self.assertEqual(profile_data['default_country'],
                         initial_form_data['default_country'])
        self.assertEqual(profile_data['default_name'],
                         initial_form_data['default_name'])

    def test_invalid_order_form_returns_message(self):
        # Add an item to session['bag']
        add_to_bag_url = reverse('add_to_bag', args=[self.album.slug])
        self.client.post(add_to_bag_url, data={
            'quantity': 1,
            'format': 'cd',
        })
        form_data = {
            'name': '',
            'email': '',
            'phone_number': '',
            'address_line1': '',
            'address_line2': '',
            'town_or_city': '',
            'county': '',
            'postcode': '',
            'country': '',
        }
        checkout_url = reverse('checkout')
        response = self.client.post(checkout_url, data=form_data)
        messages = list(response.wsgi_request._messages)
        # Expect 2 messages - The first will be confirmation of adding the
        # album to the bag
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]),
                         ('There is an issue with your information,'
                          ' please check the form and try again.'))

    def test_missing_profile_on_checkout_returns_order_form(self):
        new_user = User.objects.create_user(username='new_test_user',
                                            email='new_test_email@email.com',
                                            password='test_password')
        self.client.login(
            username='new_test_user',
            password='test_password'
            )
        # Add an item to session['bag']
        add_to_bag_url = reverse('add_to_bag', args=[self.album.slug])
        self.client.post(add_to_bag_url, data={
            'quantity': 1,
            'format': 'cd',
        })
        url = reverse('checkout')
        # Get the new_user's Profile and delete
        profile = Profile.objects.get(user=new_user)
        profile.delete()
        # Ensure the view raises the Profile.DoesNotExist exception
        response = self.client.get(url)
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(user=response.wsgi_request.user)
        self.assertIsInstance(response.context['form'], OrderForm)

    def test_product_order_line_item_updates_order_total_on_delete(self):
        # Get the order containing the line items created in SetUp
        order = Order.objects.get(name='Test User',
                                  email='test@email.com')

        # Get the initial grand total of the order
        initial_total = order.grand_total

        # Delete the ProductOrderLineItem and ensure the related
        # order grand total is now £9.99 less than before
        product_line_item = order.productlineitems.first()
        product_line_item.delete()

        new_total = round(order.grand_total, 2)

        self.assertEqual(new_total,
                         initial_total - round(Decimal(9.99), 2))

    def test_album_order_line_item_updates_order_total_on_delete(self):
        # Get the order containing the line items created in SetUp
        order = Order.objects.get(name='Test User',
                                  email='test@email.com')

        # Get the initial grand total of the order
        initial_total = order.grand_total

        # Delete the ProductOrderLineItem and ensure the related
        # order grand total is now £9.99 less than before
        album_line_item = order.albumlineitems.first()
        album_line_item.delete()

        new_total = round(order.grand_total, 2)

        self.assertEqual(new_total,
                         initial_total - round(Decimal(9.99), 2))
