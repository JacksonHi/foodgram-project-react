from django.contrib import admin
from api.models import MeasurementUnit, Ingredients, Tag, Recipe


class MeasurementUnitAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'measurement_unit')
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    search_fields = ('title',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'tag', 'cooking_time')
    search_fields = ('title',)


admin.site.register(MeasurementUnit, MeasurementUnitAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
