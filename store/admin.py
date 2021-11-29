from django.contrib import admin
from django.utils.safestring import mark_safe

from store.models import Genres, Games


class GenresFilter(admin.SimpleListFilter):
    title = 'genres'
    parameter_name = 'genres'

    def lookups(self, request, model_admin):
        return set([(genre.slug, genre.name) for genre in Genres.objects.all()])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(genres__slug=self.value())


class GenresAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class GamesAdmin(admin.ModelAdmin):
    list_display = ['view_poster', 'id', 'name', 'slug', 'price', 'stock', 'created_at', 'updated_at']
    list_filter = [GenresFilter, 'created_at', 'updated_at']
    list_editable = ['price', 'stock']
    prepopulated_fields = {'slug': ('name',)}

    @staticmethod
    def view_poster(obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="60">')


admin.site.register(Genres, GenresAdmin)
admin.site.register(Games, GamesAdmin)
