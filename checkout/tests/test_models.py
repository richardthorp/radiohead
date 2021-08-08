from decimal import Decimal
from django.test import TestCase
from shop.models import Album, Product
from ..models import Order, ProductOrderLineItem, AlbumOrderLineItem


class TestCheckoutModels(TestCase):
    def setUp(self):
        test_order = {
            "email": 'test_user@test.com',
            "name": 'Test User',
            "phone_number": 12345678901,
            "address_line1": 'Test Line 1',
            "address_line2": 'Test Line 2',
            "town_or_city": 'Test Town',
            "county": 'Test County',
            "postcode": 'POSTCODE',
            "country": 'GB',
            "original_bag": {
                "test_album": {
                    "type": 'album',
                    "items_by_format": {"cd": 1}}},
            "stripe_pid": 'testpid'
        }
        self.order = Order.objects.create(**test_order)

        test_album = {
            "title": 'test_album',
            "year": 2021,
            "cd_price": 10,
            "vinyl_price": 20,
            "spotify_url": 'www.testurl.com',
            "tracklist": {"test": "test"},
            "image": 'media_files/album_covers/kid_a_cover.jpg'
            }
        self.album = Album.objects.create(**test_album)

        test_product = {
            "name": 'test_item',
            "category": 'clothing',
            "price": 5,
            "image": 'test_image.jpg'
        }
        self.product = Product.objects.create(**test_product)

        test_album_order_line_item = {
            'order': self.order,
            'album': self.album,
            'format': 'cd',
            'quantity': 1,
        }
        self.album_line_item = AlbumOrderLineItem.objects.create(
            **test_album_order_line_item)

        test_product_order_line_item = {
            'order': self.order,
            'product': self.product,
            'size': 'S',
            'quantity': 1,
        }
        self.product_line_item = ProductOrderLineItem.objects.create(
            **test_product_order_line_item)

    # Order Model Tests
    def test_order_str_method(self):
        order_number = self.order.order_number
        self.assertEqual(str(self.order), f'Order: {order_number}')

    def test_generate_order_number_returns_correct_format(self):
        order_number = self.order._generate_order_number()
        self.assertEqual(len(order_number), 32)
        self.assertIsInstance(order_number, str)

    # AlbumOrderLine Item Model with CD
    def test_add_cd_album_line_item_total_updates_order_total(self):
        # Test the initial order costs - Order has 2 items,
        # 1 x CD (£10), 1 Product (£5) and delivery fee of £4.99
        self.assertEqual(self.order.order_total, 15)
        self.assertEqual(float(self.order.delivery_cost), 4.99)
        self.assertEqual(float(self.order.grand_total), 19.99)

        # Create a new cd album order line item on the Order and save
        new_album_order_line_item = {
            'order': self.order,
            'album': self.album,
            'format': 'cd',
            'quantity': 1,
        }
        album_line_item = AlbumOrderLineItem.objects.create(
            **new_album_order_line_item)
        album_line_item.save()

        # Updated order should have 3 items, 2 x CD (£20), 1 x Product (£5)
        # and delivery fee of £0
        self.assertEqual(self.order.order_total, 25)
        self.assertEqual(float(self.order.delivery_cost), 0)
        self.assertEqual(float(self.order.grand_total), 25)

    # AlbumOrderLine Item Model with Vinyl
    def test_add_vinyl_album_line_item_total_updates_order_total(self):
        # Test the initial order costs - Order has 2 items,
        # 1 x CD (£10), 1 Product (£5) and delivery fee of £4.99
        self.assertEqual(self.order.order_total, 15)
        self.assertEqual(float(self.order.delivery_cost), 4.99)
        self.assertEqual(float(self.order.grand_total), 19.99)

        # Create a new vinyl album order line item on the Order and save
        new_album_order_line_item = {
            'order': self.order,
            'album': self.album,
            'format': 'vinyl',
            'quantity': 1,
        }
        album_line_item = AlbumOrderLineItem.objects.create(
            **new_album_order_line_item)
        album_line_item.save()

        # Updated order should have 3 items, 1 x CD (£10), 1 x Vinyl (£20)
        # 1 x Product (£5) and delivery fee of £0
        self.assertEqual(self.order.order_total, 35)
        self.assertEqual(float(self.order.delivery_cost), 0)
        self.assertEqual(float(self.order.grand_total), 35)

    # ProductOrderLine Item Model
    def test_add_product_line_item_total_updates_order_total(self):
        # Test the initial order costs - Order has 2 items,
        # 1 x CD (£10), 1 Product (£5) and delivery fee of £4.99
        self.assertEqual(self.order.order_total, 15)
        self.assertEqual(float(self.order.delivery_cost), 4.99)
        self.assertEqual(float(self.order.grand_total), 19.99)

        # Create a new album order line item on the Order and save
        new_product_order_line_item = {
            'order': self.order,
            'product': self.product,
            'size': 'M',
            'quantity': 1,
        }
        product_line_item = ProductOrderLineItem.objects.create(
            **new_product_order_line_item)
        product_line_item.save()

        # Updated order should have 3 items, 1 x CD (£10), 2 x Product (£10)
        # and delivery fee of £4.99
        self.assertEqual(self.order.order_total, 20)
        self.assertEqual(float(self.order.delivery_cost), 4.99)
        self.assertEqual(float(self.order.grand_total), 24.99)

    # AlbumOrderLineItem __str__ method
    def test_album_order_line_item_str_method(self):
        expected_str = (f'Album in order {self.order.order_number} - '
                        f'{self.album.title}, '
                        f'{self.album_line_item.quantity}: '
                        f'{self.album_line_item.lineitem_total}')

        self.assertEqual(str(self.album_line_item), expected_str)

    # ProductOrderLineItem __str__ method
    def test_product_order_line_item_str_method(self):
        expected_str = (f'Line item in order {self.order.order_number} - '
                        f'{self.product.name}, '
                        f'{self.product_line_item.quantity}: '
                        f'{self.product_line_item.lineitem_total}')
        self.assertEqual(str(self.product_line_item), expected_str)
