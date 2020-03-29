from django.test import TestCase

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
        self.assertEqual(product1.code, "123456")

    def test_product_slug_create(self):
        product1 = Product.objects.get(code="123456")
        self.assertEqual(product1.slug, 'coco-colo')

    # def test_100g_proportion(self):
    #     """
    #     check if nutrition 100g is less than 100g
    #     """
    #     wrong_product = Product(fat = 101)
