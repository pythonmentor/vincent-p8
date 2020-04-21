import requests
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from .models import Product, Category


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