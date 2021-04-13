from django.urls import path

from mainapp.views import products, ProductList, ProductAdminList, main

app_name = 'mainapp'

urlpatterns = [
    path('', main, name='index'),
    path('admin_products/', ProductAdminList.as_view(), name='admin_products'),
    path('<int:category_id>/', ProductList.as_view(), name='product'),
    path('page/<int:page>/', products, name='page')
]