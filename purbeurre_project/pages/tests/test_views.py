from django.test import TestCase
from django.urls import reverse, resolve
from pages import views


#########################
#    TEST INDEX         #
#########################
class TestPages(TestCase):

    def test_index_view(self):
        response = self.client.get('/')
        # User open home page
        self.assertEqual(response.status_code, 200)
        # it is resolved to a function
        self.assertEqual(response.resolver_match.func, views.index)
        # a template is dedicated for that
        self.assertEqual(response.templates[0].name, 'pages/index.html')

    def test_legals(self):
        url = reverse('pages:legals')
        response = self.client.get(url)
        # User open home page
        self.assertEqual(response.status_code, 200)
        # it is resolved to a function
        self.assertEqual(response.resolver_match.func, views.legals)
        # a template is dedicated for that
        self.assertEqual(response.templates[0].name, 'pages/legals.html')

