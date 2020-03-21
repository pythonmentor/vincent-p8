import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product

API_URL = 'https://fr-en.openfoodfacts.org/cgi/search.pl?'
USER = 'vft'
SEARCH_HEADER = {
    "user-agent": "Purbeurre - https://github.com/finevine/Projet8"
    }

@login_required(login_url='/accounts/login/')
def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        products = ['produit 1', 'produit 2', 'produit 3']
        context = {'products': products}
        return render(request, 'products/index.html', context)


def search(request):
    ''' This function get the products of a category
    and return them as a list of Product_API '''
    # list of product to output
    products = []
    # initialize to page 1 of search result
    page = 1
    search_param = {"search_terms": + request.field,
                "search_simple": 1,
                "sort_by": "unique_scans_n",
                "action": "process",
                "json": 1}
    req = requests.get(
        API_URL,
        params = search_param,
        headers = SEARCH_HEADER)
    # output of request as a json file
    req_output = req.json()
    # list of product of the output
    products_output = req_output['products']
    # store product classes
    for product in products_output:
        code = product.get('code', '')
        name = product.get('product_name', '')
        nutritionGrade = product.get('nutriscore_grade', '')
        image = product.get('selected_images', '')['front']['display']['fr']
        fat = product.get('nutriments', '')['fat_100g']
        satFat = product.get('nutriments', '')['saturated-fat_100g']
        sugar = product.get('nutriments', '')['sugar_100g']
        salt = product.get('nutriments', '')['salt_100g']
        compared_to_category = product.get("compared_to_category", '')
        new_prod = Product(
            code = code,
            name = name,
            nutritionGrade = nutritionGrade,
            image = image,
            fat = fat,
            satFat = satFat,
            sugar = sugar,
            salt = salt,
            compared_to_category = compared_to_category
            )
        new_prod.save()

    return HttpResponseRedirect(reverse('products:results', request.field))
