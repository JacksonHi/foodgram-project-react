from encodings import search_function
from re import search
from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from .models import Recipe, Tag


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if value:
            """return Recipe.objects.filter(
                favourite__author=self.request.user.id
            ).order_by('-id')"""
            return queryset.filter(favourite__author=self.request.user.id)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            """return Recipe.objects.filter(
                basket__author=self.request.user.id
            ).order_by('-id')"""
            return queryset.filter(basket__author=self.request.user.id)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart',)
