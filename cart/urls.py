from django.urls import path

from cart.views import cart_add, CartDetail, cart_remove, update_qty

app_name = 'cart'

urlpatterns = [
    path('', CartDetail.as_view(), name='cart_detail'),
    path('add/<int:game_id>/', cart_add, name='cart_add'),
    path('remove/<int:game_id>/', cart_remove, name='cart_remove'),
    path('ajax/', update_qty, name='up_qty')
]
