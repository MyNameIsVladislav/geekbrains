from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from accounts.models import User
from accounts.forms import UserLoginForm, UserRegisterForm, UserEditForm, EditProfileForm
from accounts.utils import send_verify_mail


profile_menu = [
    {'title': 'Аккаунт', 'url': 'edit', 'namespace': 'auth:edit'},
    {'title': 'Личные данные', 'url': 'profile', 'namespace': 'auth:profile'}
]


def login(request):
    title = 'Авторизация'
    print(request.user)

    login_form = UserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        email = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))

    content = {'title': title, 'login_form': login_form}
    return render(request, 'registration/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    title = 'Registration'

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            user = register_form.save()
            user.is_active = False
            user.save()
            if send_verify_mail(user):
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:login'))
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
