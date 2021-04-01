from django.urls import path

from mainapp.views import products, ProductList

app_name = 'mainapp'

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('<int:category_id>/', ProductList.as_view(), name='product'),
    path('page/<int:page>/', products, name='page')
]