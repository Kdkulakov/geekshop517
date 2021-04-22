from django.test import TestCase, Client

from mainapp.models import ProductCategory, Product


class TestMainappTestCase(TestCase):

    def setUp(self):
        category = ProductCategory.objects.create(
            name='TestCat1'
        )
        Product.objects.create(
            category=category,
            name='product_test_1'
        )
        Product.objects.create(
            category=category,
            name='product_test_2'
        )
        Product.objects.create(
            category=category,
            name='product_test_3'
        )
        self.client = Client()

    def test_mainapp_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_mainapp_shop(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/{category.pk}/')
            self.assertEqual(response.status_code, 200)

        for product in Product.objects.all():
            response = self.client.get(f'/products/detail/{product.pk}/')
            self.assertEqual(response.status_code, 200)
