from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

from django.urls import reverse, reverse_lazy

from accounts.models import User
from accounts.forms import UserLoginForm, UserRegisterForm, UserEditForm, EditProfileForm
from accounts.service import registration_form


profile_menu = [
    {'title': 'Аккаунт', 'url': 'edit', 'namespace': 'auth:edit'},
    {'title': 'Личные данные', 'url': 'profile', 'namespace': 'auth:profile'}
]


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse_lazy('main:index'))
    form = UserLoginForm()
    return render(request, "registration/login.html", {'login_form': form})


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


def valid_password(request):
    token, email, password = request.POST.values()
    user = authenticate(request, email=email, password=password)
    context = {'status': False}
    if user:
        login(request, user)
        messages.success(request, "Logged In")
        context['status'] = True
    else:
        context['message'] = 'invalid login or password'
    return JsonResponse(context, status=200)
