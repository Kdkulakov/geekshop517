from django.urls import path

from adminapp.views import index, UserListView, UserCreateView, UserUpdateView, UserDeleteView, ProductCategoryList, \
    ProductCategoryUpdate, ProductCategoryDelete

app_name = 'adminapp'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admin_users'),
    path('users-create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='admin_users_update'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(), name='admin_users_delete'),
    path('categories/', ProductCategoryList.as_view(), name='admin_categories_list'),
    path('category/update/<int:pk>/', ProductCategoryUpdate.as_view(), name='admin_category_update'),
    path('category/delete/<int:pk>/', ProductCategoryDelete.as_view(), name='admin_category_delete'),
]
