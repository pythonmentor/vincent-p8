from unittest.mock import patch
from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from products import views
from products.models import Product, Category, Favourite

# from .mock import OPENFF_REQUEST

#########################
#    TEST 404
#########################
class Test404(SimpleTestCase):

    def test_404_view(self):
        response = self.client.get('/false_URL')
        # User open a wrong url
        self.assertEqual(response.status_code, 404)
        # a template is dedicated for that
        self.assertEqual(response.templates[0].name, '404.html')


#########################
#  TEST SAVE / DELETE
#########################
class TestSaveDelete(TestCase):

    @classmethod  # <- setUpTestData must be a class method
    def setUpTestData(cls):
        # create one category for all products created
        Category.objects.create(id="fruits:fr", name="Fruits frais")
        cls.category = Category.objects.get(id="fruits:fr")
        # create 2 products
        for i in range(2):
            Product.objects.create(
                name="prod"+str(i),
                code=str(i),
                nutritionGrade='b',
                category=cls.category)
        # create a user just for this test
        cls.user1 = User.objects.create_user(
            'user1name',
            'user1@email.com',
            'user1password')
        cls.prod1 = Product.objects.get(code=1)

    def setUp(self):
        self.client.login(username='user1name', password='user1password')

    def test_save(self):
        ''' save redirect and actually save Favourite '''
        # SAVE url to call with a post
        url = reverse('products:save', kwargs={'pk_health': 0, 'pk_unhealth': 1})
        response = self.client.post(url, {}, HTTP_REFERER='http://mytest')

        # And get redirected to the same origin page
        self.assertRedirects(
            response,
            'http://mytest',
            fetch_redirect_response=False,
            status_code=302,
            target_status_code=200)

        self.assertTrue(
            Favourite.objects.filter(
                    healthy_product=0,
                    unhealthy_product=1,
                    owner=self.user1,
                    ).exists())

    def test_delete(self):
        # First save Favourite
        self.test_save()

        # Then DELETE
        url = reverse('products:delete', kwargs={'pk_health': 0, 'pk_unhealth': 1})
        response = self.client.post(url, {}, HTTP_REFERER='http://mytest')

        self.assertRedirects(
            response,
            'http://mytest',
            fetch_redirect_response=False,
            status_code=302,
            target_status_code=200)

        self.assertFalse(
            Favourite.objects.filter(
                    healthy_product=0,
                    unhealthy_product=1,
                    owner=self.user1,
                    ).exists())


#########################
#     TEST SEARCH
#########################
class TestSearch(TestCase):

    @patch('products.models.ProductManager.similar')
    def test_ProductsView(self, mock_similar):
        mock_category = Category(id="fruits:fr", name="Fruits")
        mock_similar.return_value = [Product(code='1234', name='toto', category=mock_category)]
        url = reverse('products:search')
        response = self.client.get(url, data={'q': 'toto'})
        self.assertContains(response, 'Toto')


#########################
#    TEST FAVORITES
#########################
# test FavouritesView for learning purpose, we keep ORM calls in these tests
class TestFavouritesView(TestCase):

    def test_index_url_resolves(self):
        ''' products:index url call views.index '''
        # create a user just for this test
        self.user1 = User.objects.create_user(
            'user1name',
            'user1@email.com',
            'user1password')
        self.client.login(username='user1name', password='user1password')
        url = reverse('products:index')
        # Compare name of functions because
        # functions generated by as_view()
        # won't be equal due to different object ids
        self.assertIs(
            resolve(url).func.__name__,
            views.FavouritesView.as_view().__name__)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'user1name')
        self.assertTemplateUsed(response, 'products/favourites_list.html')

    def test_anonymousUser_open_index(self):
        # Someone tries to open products index
        url = reverse('products:index')
        webpage = self.client.get(url)

        # As an anonymousUser
        self.assertEqual(
            webpage.context,
            None)
        # And get redirected to login
        self.assertRedirects(
            webpage,
            reverse('login')+'?next='+url,
            status_code=302,
            target_status_code=200)


#########################
#    TEST COMPARE
#########################
class TestCompare(TestCase):

    @classmethod  # <- setUpTestData must be a class method
    def setUpTestData(cls):
        # create one category for all products created
        Category.objects.create(
            id="fruits:fr",
            name="Fruits frais")
        cls.category = Category.objects.get(id="fruits:fr")
        # create 15 products
        for i in range(15):
            Product.objects.create(
                name="prod"+str(i),
                code=str(i),
                nutritionGrade='b',
                category=cls.category)
        # create one unhealthy product to check filtering
        Product.objects.create(
                name="lastprod",
                code='67890',
                nutritionGrade='e',
                category=cls.category)
        cls.prod1 = Product.objects.get(code=1)


    def test_compare_resolves(self):
        url = reverse(
            'products:compare',
            args=[self.category.id])
        response = self.client.get(
            url,
            data={'code': self.prod1.code})
        self.assertEqual(response.status_code, 200)
        # Test if response contains product searched (capitalized)
        self.assertContains(response, 'Prod1')

    def test_pagination_is_twelve(self):
        url = reverse(
            'products:compare',
            args=[self.category.id])
        response = self.client.get(
            url,
            data={'code': self.prod1.code})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['product_list']) == 12)

    def test_lists_all_candidates(self):
        '''
        Get second page and confirm it has exactly remaining (15-1-12=2) items
        '''
        url = reverse('products:compare', args=[self.category.id])
        response = self.client.get(
            url,
            data={'code': self.prod1.code, 'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['product_list']) == 2)


#########################
#     TEST DETAIL
#########################
class TestDetail(TestCase):

    def test_ProductDetailView2(self):
        mock_category = Category(id="fruits:fr", name="Fruits")
        mock_product = Product(code='5', name='prod5', category=mock_category)

        # Patch genericView to return only one object
        with patch.object(
            views.ProductDetailView,
            'get_object',
            return_value=mock_product):

                url = reverse('products:detail', args=[5])
                response = self.client.get(url)
                # Test function used
                self.assertIs(
                    resolve(url).func.__name__,
                    views.ProductDetailView.as_view().__name__)
                # Test template used
                self.assertTemplateUsed(response, 'products/product_detail.html')
                self.assertContains(response, 'Prod5')
