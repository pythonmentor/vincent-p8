
from unittest.mock import Mock, patch
from django.test import TestCase, SimpleTestCase
from products.views import get_openff_products
from .mock import OPENFF_REQUEST


class TestViews(SimpleTestCase):

    @patch('products.views.requests.get')
    def test_get_openff_products(self, mock_get):
        '''
        get_openff_products() return list of products provided by OpenFoodFacts.
        '''
        # Configure the mock to return a response with an OK status code.
        # Also, the mock has a `json()` method that returns a list of products.
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = OPENFF_REQUEST
        # Call the service, which will send a request to the server.
        response = get_openff_products('toto')

        # If the request is sent successfully, then a response is expected.
        self.assertEquals(response, OPENFF_REQUEST['products'])

    @patch('products.views.requests.get')
    def test_get_openff_products_when_response_is_NOK(self, mock_get):
        '''
        get_openff_products() return None when API OpenFoodFacts status is not 200.
        '''
        # Configure the mock to not return a response with NOK status code.
        mock_get.return_value.codes = False
        # Call the service, which will send a request to the server.
        response = get_openff_products('toto')
        # If the response contains an error, no products are expected.
        self.assertEquals(response, None)
