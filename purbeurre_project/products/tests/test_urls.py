from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve

from products.views import index, search

# Create your tests here.
# https://www.youtube.com/watch?v=0MrgsYswT1c&list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM&index=2

class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('productsindex')
        self.assertIs(resolve(url).func, index)
