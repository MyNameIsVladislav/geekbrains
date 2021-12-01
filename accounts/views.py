from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from accounts.models import User
from accounts.forms import UserLoginForm, UserRegisterForm
from accounts.utils import send_verify_mail


def login(request):
    title = 'Авторизация'

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
        auth.login(request, user)
        return render(request, 'registration/verification.html')
    else:
        print(f'error activation user: {user}')
        return render(request, 'registration/verification.html')
