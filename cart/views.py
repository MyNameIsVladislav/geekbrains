from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from store.models import Games
from cart.models import Cart
from cart.forms import CartAddProductForm


@login_required
def cart_add(request, game_id):
    cart = Cart(request)
    product = get_object_or_404(Games, id=game_id)
    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
    else:
        cart.add(product=product, update_quantity=True)
    return redirect('cart:cart_detail')


@login_required
def cart_remove(request, game_id):
    cart = Cart(request)
    product = get_object_or_404(Games, id=game_id)
    cart.remove(product)
    if request.GET.get('del', None):
        return HttpResponseRedirect(reverse('order:not_product', args=(product.id,)))
    return redirect('cart:cart_detail')


class CartDetail(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return render(request, 'cart/detail.html', {'cart': cart})
