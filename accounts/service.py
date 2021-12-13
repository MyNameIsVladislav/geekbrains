from django.urls import reverse
from django.http import HttpResponseRedirect

from accounts.utils import send_verify_mail


def registration_form(register_form):
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
