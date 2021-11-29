from django.db import models
from django.urls import reverse

from store.utils import get_path


class Genres(models.Model):

    class Meta:
        db_table = 'genres'
        verbose_name = 'Жанр'
        verbose_name_plural = "Жанры"

    name = models.CharField(verbose_name="Жанр", max_length=14)
    slug = models.SlugField(verbose_name='URL')

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('store:genres', kwargs={'slug_genre': self.slug})


class Games(models.Model):

    class Meta:
        db_table = 'games'
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    name = models.CharField(verbose_name='Название', max_length=70)
    slug = models.SlugField(verbose_name='URL')
    genres = models.ManyToManyField(Genres, related_name='genre', related_query_name='genres')

    poster = models.ImageField(verbose_name='Постер', upload_to=get_path)
    banner = models.ImageField(verbose_name='Баннер', upload_to=get_path)

    describe = models.TextField(max_length=300)

    price = models.PositiveIntegerField(verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='Количество товара')

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{id} - {self.name}'

    def get_absolute_url(self):
        return reverse('store:game', kwargs={'pk': self.pk})
