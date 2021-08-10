import stripe
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
            'name': 'Test User',
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

        # Ensure an order has been created
        orders = Order.objects.all()
        self.assertEqual(len(orders), 1)

        # Check AlbumOrderLineItem has been created
        album_line_items = AlbumOrderLineItem.objects.all()
        self.assertEqual(len(album_line_items), 1)

        # Check 2 ProductOrderLineItems have been created
        product_line_items = ProductOrderLineItem.objects.all()
        self.assertEqual(len(product_line_items), 2)

        # Get the newly created order
        order = Order.objects.first()

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
            'name': 'Test User',
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

        # Ensure an order has been created
        orders = Order.objects.all()
        self.assertEqual(len(orders), 1)

        # Ensure AlbumOrderLineItem has been created
        album_line_items = AlbumOrderLineItem.objects.all()
        self.assertEqual(len(album_line_items), 1)

        # Get the newly created order
        order = Order.objects.first()

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
            # 'user': self.user,
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

        self.assertEqual(profile_data, initial_form_data)

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
