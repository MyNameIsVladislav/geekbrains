from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse, reverse_lazy

from accounts.models import User
from accounts.forms import UserLoginForm, UserRegisterForm, UserEditForm, EditProfileForm
from accounts.service import registration_form


profile_menu = [
    {'title': 'Аккаунт', 'url': 'edit', 'namespace': 'auth:edit'},
    {'title': 'Личные данные', 'url': 'profile', 'namespace': 'auth:profile'}
]


class LoginNewView(LoginView):
    template_name = 'registration/login.html'
    form_class = UserLoginForm
    authentication_form = UserLoginForm
    success_url = reverse_lazy('main:index')
    redirect_authenticated_user = True

    def form_invalid(self, form):
        return self.get(request=self.request)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    title = 'Registration'

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        return registration_form(register_form)
    else:
        register_form = UserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'registration/register.html', content)


def verify(request, email, activation_key):
    user = User.objects.get(email=email)
    if user.activation_key == activation_key and not user.is_activation_key_expired():
        user.is_active = True
        user.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'registration/verification.html')
    else:
        print(f'error activation user: {user}')
        return render(request, 'registration/verification.html')


def edit_user(request):
    title = 'Аккаунт'
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = UserEditForm(instance=request.user)
        content = {'title': title, 'edit_form': edit_form, 'menu': profile_menu, 'namespace': 'auth:edit'}

        return render(request, 'registration/edit.html', content)


def edit_profile(request):
    title = 'Профиль'
    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('auth:profile'))

    profile_form = EditProfileForm(instance=request.user.profile)
    content = {'title': title, 'edit_form': profile_form, 'menu': profile_menu, 'namespace': 'auth:profile'}
    return render(request, 'registration/edit.html', content)
