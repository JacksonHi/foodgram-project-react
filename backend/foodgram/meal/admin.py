from django.contrib import admin
from meal.models import MeasurementUnit, Ingredients, Tag, Recipe


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'measurement_unit')
    search_fields = ('name',)

admin.site.register(MeasurementUnit)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Tag)
admin.site.register(Recipe)
