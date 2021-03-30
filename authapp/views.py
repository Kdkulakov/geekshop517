import hashlib
import random

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib import auth
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from authapp.forms import UserLoginForm, UserRegisterForm, UserEditForm
from basketapp.models import Basket
from django.views.generic import FormView, UpdateView

from .models import User


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#         else:
#             print(form.errors)
#     else:
#         form = UserLoginForm()
#     context = {'form': form}
#     return render(request, 'authapp/login.html', context)


class GeekLoginView(FormView):
    model = User
    success_url = reverse_lazy('index')
    form_class = UserLoginForm
    template_name = 'authapp/login.html'
    title = 'Login'

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(data=request.POST)
    #
    #     if form.is_valid():
    #         usr = form.cleaned_data.get('username')
    #         pwd = form.cleaned_data.get('password')
    #
    #         user = authenticate(
    #             username=usr,
    #             password=pwd
    #         )
    #
    #         if user and user.is_active:
    #             login(request, user)
    #             return redirect(self.success_url)
    #
    #     return render(request, self.template_name, {'form': form})



# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             user = form.save()
#             if send_verify_mail(user):
#                 messages.success(request, 'Вы успешно зарегистрировались!')
#                 return HttpResponseRedirect(reverse('auth:login'))
#         else:
#             print(f'ERROR form is not valid - {form.errors}')
#
#     else:
#         form = UserRegisterForm()
#     context = {'form': form}
#     return render(request, 'authapp/register.html', context)


class RegisterView(FormView):
    model = User
    form_class = UserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('auth:login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save()
            if self.send_verify_mail(user):
                messages.success(request, 'Вы успешно зарегистрировались! Проверьте почту. Активируйте учетную запись.')
                return redirect(self.success_url)

            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})

    def send_verify_mail(self, user):
        verify_link = reverse_lazy('authapp:verify', args=[user.email, user.activation_key])

        title = f'Для активации учетной записи {user.username} пройдите по ссылке'

        messages = f'Для подтверждения учетной записи {user.username} пройдите по ссылке: \n{settings.DOMAIN_NAME}' \
                   f'{verify_link}'

        return send_mail(title, messages, settings.EMAIL_HOST_USER, [user.email,], fail_silently=False)

    def verify(self, email, activation_key):
        try:
            user = User.objects.get(email=email)
            if user.activation_key == activation_key and not user.is_activation_key_expired():
                user.is_active = True
                user.save()
                auth.login(self, user)
                return render(self, 'authapp/verification.html')
            else:
                print(f'error activation user: {user}')
                return render(self, 'authapp/verification.html')
        except Exception as e:
            print(f'error activation user : {e.args}')
            return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        form = UserEditForm(instance=user)
    context = {
        'form': form,
        'baskets': Basket.objects.filter(user=user),
    }
    return render(request, 'authapp/profile.html', context)


# @login_required
# def profile(request):
#     user = request.user
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('auth:profile'))
#     else:
#         form = UserProfileForm(instance=user)
#     context = {
#         'form': form,
#         'baskets': Basket.objects.filter(user=user),
#     }
#     return render(request, 'authapp/profile.html', context)

class ProfileView(UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'authapp/profile.html'
    success_url = reverse_lazy('auth:profile')

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
