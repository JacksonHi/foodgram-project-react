from django.contrib import admin
from api.models import Ingredients, Tag, Recipe


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    search_fields = ('title',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'cooking_time')
    search_fields = ('title',)


admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
