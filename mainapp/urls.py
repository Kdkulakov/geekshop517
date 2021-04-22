from django.urls import path

from mainapp.views import ProductList, ProductAdminList, products_ajax, ProductCategoryList, ProductListByCategory, \
    ProductDetail
from django.views.decorators.cache import cache_page

app_name = 'mainapp'

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('<int:category_id>/', ProductListByCategory.as_view(), name='products_by_category'),
    path('categories/', ProductCategoryList.as_view(), name='categories'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),

    path('admin_products/', ProductAdminList.as_view(), name='admin_products'),

    path('category/<int:pk>/ajax/', cache_page(3600)(products_ajax), name='ajax'),
]