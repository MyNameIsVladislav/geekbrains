from django.db import transaction, IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string

from core.settings import EMAIL_HOST_USER
from wallet.models import PurseModel


@transaction.atomic
def pay_product(request, order, cart):
    try:
        user_wallet = PurseModel.objects.filter(user_id=request.user).first()
        user_wallet.money -= order.get_total_cost()
        user_wallet.save()
    except IntegrityError:
        return HttpResponseRedirect(reverse('order:not_money'))
    for item in order.items.all():
        try:
            item.product.stock -= item.quantity
            item.product.save()
        except IntegrityError:
            return HttpResponseRedirect("%s?del=prod" % reverse('cart:cart_remove', args=(item.product.pk,)))

    send_email_success(cart, request.user, order.email)
    order.paid = True
    order.save()
    cart.clear()
    return render(request, 'order/order_created.html')


def send_email_success(cart, user, email):
    msg_html = render_to_string('order/email.html', {'cart': cart, 'user': user})
    send_mail('Successful', msg_html, EMAIL_HOST_USER, [email], html_message=msg_html)
