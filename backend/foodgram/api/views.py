from rest_framework import viewsets
from .models import Ingredients, Tag, Recipe, AmountOfIngredients
from .serializers import IngredientsSerializer, TagSerializer, RecipeSerializer, AmountOfIngredientsSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    """def create(self, request, *args, **kwargs):
        #print(request.data)
        recipe = request.data['name']
        ingredients = request.data['ingredients']
        new_ingredients = []
        for ingredient in ingredients:    # перебираю список ингредиентов
            ingredient = Ingredients.objects.get(id=ingredient['id'])   # запрос на получение списка ингредиентов
            #print(ingredient)
            ingredient = {'name': ingredient.name, 'measurement_unit': ingredient.measurement_unit}
            new_ingredients.append(ingredient)

            # создать экземпляр игнредиента с колиреством и рецептом
        #print(new_ingredients)
        request.data['ingredients'] = new_ingredients
        print(request.data)
        return super().create(request, *args, **kwargs)"""

    def perform_create(self, serializer):
        #print(serializer)
        serializer.save(
            author=self.request.user
            )
