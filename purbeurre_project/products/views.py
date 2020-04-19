import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
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
    name = request.GET['q']
    # faire une vue générique avec une liste
    return HttpResponse(
        Product.objects.filter(Q(name__contains=name)|Q(category__name__contains=name))
        )


class ProductsView(generic.ListView):
    model = Product

    def get_context_data(self, **kwargs):
        name = self.request.GET.get('q')
        context = super().get_context_data(**kwargs)
        # name to find in product name or category
        queryset = Product.objects.filter(Q(name__contains=name)|Q(category__name__contains=name))
        context['products_found'] = queryset
        return context
