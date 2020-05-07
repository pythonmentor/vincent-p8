import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from .models import Product, Category, Favourite


@login_required(login_url='/accounts/login/')
def index(request):
    favourites = Favourite.objects.filter(owner = request.user)
    context = {'favourites': favourites}
    return render(request, 'products/favourites.html', context)


def search(request):
    name = request.GET['q']
    # faire une vue générique avec une liste
    return HttpResponse(
        Product.objects.filter(Q(name__contains=name)|Q(category__name__contains=name))
        )

@login_required(login_url='/accounts/login/')
def save(request, pk_health, pk_unhealth):
    ''' parameter are defined in the url path '''
    healthy_product = Product.objects.get(code=pk_health)
    unhealthy_product = Product.objects.get(code=pk_unhealth)
    try:
        favourite = Favourite(healthy_product=healthy_product, unhealthy_product=unhealthy_product, owner = request.user)
        favourite.save()
    except IntegrityError:
        pass
    # virgule parceque c'est un tuple
    return HttpResponseRedirect(reverse('product_detail', args=(healthy_product.code,)))


class ProductsView(generic.ListView):
    ''' query string : "q" product to find'''
    model = Product
    paginate_by = 12

    def get_queryset(self):
        name = self.request.GET.get('q')
        return Product.objects.filter(Q(name__contains=name)|Q(category__name__contains=name))

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         # name to find in product name or category
         context['query'] = self.request.GET.get('q')
         return context


@method_decorator(login_required, name='dispatch')
class FavouritesView(generic.ListView):
    ''' query string : "q" product to find'''
    model = Favourite
    paginate_by = 12
    template_name = 'products/favourites_list.html'

    def get_queryset(self):
        return Favourite.objects.filter(owner=self.request.user)
   

class CompareView(generic.ListView):
    '''
    parameter : "category:id"
    querystring : "code" product to compare
    '''
    model = Product
    paginate_by = 12
    template_name = 'products/compare_list.html'

    def get_queryset(self):
        # get captured parameter from url pattern:
        self.category = get_object_or_404(Category, id=self.kwargs['category'])
        # product to replace
        self.product_to_replace = Product.objects.get(code=self.request.GET.get('code'))
        # nutritiongrade to compare
        nutrition_compare = self.product_to_replace.nutritionGrade
        products = Product.objects.filter(category__name=self.category)
        # products must be differents from product_to_replace :
        products = products.exclude(code=self.product_to_replace.code)
        return products.filter(nutritionGrade__lte=self.product_to_replace.nutritionGrade).order_by('nutritionGrade')

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         # name to find in product name or category
         context['category'] = self.category
         context['product_to_replace'] = self.product_to_replace
         context['headerImg'] = self.product_to_replace.image
         return context

class ProductDetailView(generic.DetailView):
    '''
    parameter : "product:code"
    '''
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headerImg'] = self.object.image
        return context