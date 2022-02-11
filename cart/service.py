from django.shortcuts import get_object_or_404

from store.models import Games
from cart.models import Cart


class ServiceCart:

    def __init__(self, request, pk):
        self.request = request
        self.pk = pk

    def get_cart(self):
        return Cart(self.request)

    def total_quantity(self):
        return len(self.get_cart())

    def get_product(self):
        return get_object_or_404(Games, pk=self.pk)

    def add_to_cart(self, qty):
        self.get_cart().add(self.get_product(), update_quantity=False, quantity=qty)

    def total_price(self, qty):
        return self.get_product().price * qty

    def final_price(self):
        return self.get_cart().get_total_price()


def get_update_data(request, pk, qty):
    data = ServiceCart(request, pk)
    data.add_to_cart(qty)
    return {
        'status': True,
        'price': data.total_price(qty),
        'final_price': data.final_price(),
        'total_qty': data.total_quantity()
    }
