from django.urls import path

from order import views


app_name = 'order'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='create'),
    path('not-items/<int:prod_id>', views.NotProductView.as_view(), name='not_product'),
    path('not-money/', views.NotMoneyView.as_view(), name='not_money')
    ]
