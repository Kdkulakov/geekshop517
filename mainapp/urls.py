from django.urls import path

from mainapp.views import products, ProductList, ProductAdminList, products_ajax
from django.views.decorators.cache import cache_page

app_name = 'mainapp'

urlpatterns = [
    path('category/<int:pk>/ajax/', cache_page(3600)(products_ajax), name='ajax'),
    path('', ProductList.as_view(), name='index'),
    # path('', get_products, name='index'),
    path('admin_products/', cache_page(3600)(ProductAdminList.as_view()), name='admin_products'),
    path('<int:category_id>/', ProductList.as_view(), name='product'),
    path('page/<int:page>/', products, name='page')
]