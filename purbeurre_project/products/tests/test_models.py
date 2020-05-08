from django.test import TestCase
from django.db.utils import IntegrityError
from products.models import Product


class TestProductsModels(TestCase):

    def setUp(self):
        ''' Create product '''
        Product.objects.create(name="Coco colo", code="123456")
        # Or we can write : self.product1 = Product.object
        # but here we use a get

    def test_product_created(self):
        product1 = Product.objects.get(code="123456")
        self.assertEqual(product1.name, "Coco colo")
        self.assertEqual(product1.code, 123456)

    def test_product_slug_create(self):
        product1 = Product.objects.get(code="123456")
        self.assertEqual(product1.slug, 'coco-colo-123456')


class TestDoubleCode(TestCase):

    def setUp(self):
        ''' Create products '''
        Product.objects.create(name="Coca cola", code="123456")
        Product.objects.create(name="Coci coli", code="4566")
        Product.objects.create(name="Cocu colu", code="87745")

    def test_double_created(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(name="Coco colo", code="123456")


    # def test_100g_proportion(self):
    #     """
    #     check if nutrition 100g is less than 100g
    #     """
    #     wrong_product = Product(fat = 101)
