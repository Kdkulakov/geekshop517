from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from mainapp.models import Product, ProductCategory
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products(request):
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


# функции = вьюхи = контроллеры
def index(request):
    context = {'title': 'GeekShop'}
    return render(request, 'mainapp/index.html', context)

@cache_page(3600)
def products(request, category_id=None, page=1):
    context = {'title': 'GeekShop - Каталог', 'categories': ProductCategory.objects.all()}
    if category_id:
        products = Product.objects.filter(category_id=category_id).order_by('-price')
    else:
        products = Product.objects.all().order_by('-price')
    paginator = Paginator(products, 3)
    products_paginator = paginator.page(page)
    context.update({'products': products_paginator})
    return render(request, 'mainapp/products.html', context)


class ProductList(ListView):
    """
    Контроллер вывода списка товаров
    """
    model = Product
    template_name = 'mainapp/products.html'
    context_object_name = 'products'
    paginate_by = "3"


class ProductCategoryList(ListView):
    """
    Контроллер вывода списка категорий
    """
    model = ProductCategory
    template_name = 'mainapp/category_list.html'
    context_object_name = 'categories'
    paginate_by = "3"


class ProductAdminList(LoginRequiredMixin, ListView):
    """
    Контроллер вывода списка товаров для админки
    """
    model = Product
    template_name = 'mainapp/products_list_admin.html'
    context_object_name = 'products'
    paginate_by = "3"


def products_ajax(request, pk=None, page=1):

    links_menu = get_links_menu()

    if pk:
        if pk == '0':
            category = {
               'pk': 0,
               'name': 'все'
            }
            products = get_products_ordered_by_price()
        else:
            category = get_category(pk)
            products = get_products_in_category_ordered_by_price(pk)

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
           'links_menu': links_menu,
           'category': category,
           'products': products_paginator,
        }

        result = render_to_string(
                    'mainapp/products_list_inc.html',
                    context=content,
                    request=request)

        return JsonResponse({'result': result})