from django.views.generic import ListView, DetailView

from store.models import Games, Genres
from cart.forms import CartAddProductForm


class GamesListGenresView(ListView):
    model = Games
    template_name = 'store/catalog.html'
    context_object_name = 'game'
    allow_empty = True

    def get_queryset(self):
        if self.kwargs['slug_genres'] == 'all':
            return self.model.objects.all()
        else:
            self.allow_empty = False
            return self.model.objects.filter(
                genres__slug=self.kwargs['slug_genres'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GamesListGenresView, self).get_context_data(**kwargs)
        context['genres'] = Genres.objects.all()
        return context


class GameDetailView(DetailView):
    model = Games
    template_name = 'store/game.html'
    slug_url_kwarg = 'pk'
    context_object_name = 'game'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GameDetailView, self).get_context_data(**kwargs)
        context['categories'] = Genres.objects.all()
        context['cart_product_form'] = CartAddProductForm()
        return context
