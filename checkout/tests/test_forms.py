from django.test import TestCase
from ..forms import OrderForm


class TestCheckoutForm(TestCase):
    def test_valid_checkout_form_is_valid(self):
        form = OrderForm({
            'email': 'test@test.com ',
            'name': 'Test User',
            'phone_number': '12345678901',
            'address_line1': 'Test Line 1',
            'address_line2': 'Test Line 2',
            'town_or_city': 'Test Town',
            'county': 'Test County',
            'postcode': 'POSTCODE',
            'country': 'GB',
        })

        self.assertTrue(form.is_valid())

    def test_required_fields_are_required_in_order_form(self):
        form = OrderForm({
            'email': '',
            'name': '',
            'phone_number': '',
            'address_line1': '',
            'address_line2': '',
            'town_or_city': '',
            'county': '',
            'postcode': '',
            'country': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['email'],
                          ['This field is required.'])
        self.assertEquals(form.errors['name'],
                          ['This field is required.'])
        self.assertEquals(form.errors['phone_number'],
                          ['This field is required.'])
        self.assertEquals(form.errors['address_line1'],
                          ['This field is required.'])
        self.assertEquals(form.errors['town_or_city'],
                          ['This field is required.'])
        self.assertEquals(form.errors['country'],
                          ['This field is required.'])
