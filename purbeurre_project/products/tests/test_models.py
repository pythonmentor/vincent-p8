import datetime

from django.test import TestCase
from django.utils import timezone

from . models import Product


class ProductsModelTests(TestCase):

    def test_100g_proportion(self):
        """
        check if nutrition 100g is less than 100g
        """
        wrong_product = Product(fat = 101)
