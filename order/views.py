from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from order.models import OrderItem
from order.forms import OrderCreateForm
from order.service import pay_product
from cart.models import Cart
from store.models import Games


class NotProductView(TemplateView):
    template_name = 'order/not_product.html'

    def get_context_data(self, **kwargs):
        context = super(NotProductView, self).get_context_data(**kwargs)
        context['product'] = get_object_or_404(Games, id=kwargs['prod_id'])
        return context


class NotMoneyView(TemplateView):
    template_name = 'order/not_money.html'


class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = 'order/order_create.html'
    form_class = OrderCreateForm

    def get_initial(self):
        initial = {
            'user': self.request.user,
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
            'email': self.request.user.email,
        }
        return initial

    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        order.save()
        return pay_product(self.request, order, self.create_order_item(order))

    def create_order_item(self, order):
        cart = Cart(self.request)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'],
            )
        return cart
