from django.contrib import admin

from recipes.models import (AmountOfIngredients, Basket, Favourites,
                            Ingredients, Recipe, Tag)


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favourite')
    search_fields = ('name', 'author')
    list_filter = ('author', 'name', 'tags')

    def favourite(self, obj):
        favorited_count = Favourites.objects.filter(recipe=obj).count()
        return favorited_count

    favourite.short_description = 'В избранном'


class AmountOfIngredientsAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredients', 'amount')


class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('author', 'recipe')


class BasketAdmin(admin.ModelAdmin):
    list_display = ('author', 'recipe')


admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(AmountOfIngredients, AmountOfIngredientsAdmin)
admin.site.register(Favourites, FavouriteAdmin)
admin.site.register(Basket, BasketAdmin)
