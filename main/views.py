from django.shortcuts import render

from store.models import Games


def homepage(request):
    games = Games.objects.all()
    return render(request, 'base/homepage.html', context={'games': games})
