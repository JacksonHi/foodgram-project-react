from rest_framework import viewsets
from .models import Ingredients, Tag, Recipe
from .serializers import IngredientsSerializer, TagSerializer, RecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        recipe = request.data['name']
        ingredients = request.data['ingredients']
        for ingredient in ingredients:    # перебираю список ингредиентов
            ingredient = Ingredients.objects.filter(id=ingredient['id'])    # запрос на получение списка ингредиентов
            print(ingredient)
            # создать экземпляр игнредиента с колиреством и рецептом
        return super().create(request, *args, **kwargs)
