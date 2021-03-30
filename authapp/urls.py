from django.urls import path

from authapp.views import GeekLoginView, RegisterView, ProfileView, logout, profile

app_name = 'authapp'

urlpatterns = [
    path('login/', GeekLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<str:email>/<str:activation_key>/', RegisterView.verify, name='verify'),
]
