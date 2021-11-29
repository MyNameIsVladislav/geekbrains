from django.urls import path

from store import views


app_name = 'store'


urlpatterns = [
               path('catalog/<slug:slug_genres>/', views.GamesListGenresView.as_view(), name='catalog'),
               path('game/<slug:pk>/', views.GameDetailView.as_view(), name='game')
]
