from django.contrib import admin
from api.models import Ingredients, Tag, Recipe, AmountOfIngredients


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'cooking_time')
    search_fields = ('name',)


class AmountOfIngredientsAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredients', 'amount')


admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(AmountOfIngredients, AmountOfIngredientsAdmin)
