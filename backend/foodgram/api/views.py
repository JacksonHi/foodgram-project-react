from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import (AmountOfIngredients, Ingredients, Tag, Recipe,
                     Favourites, Basket)
from .serializers import IngredientsSerializer, TagSerializer, RecipeSerializer
from .pagination import RecipePagination
from .permissions import RecipePermission
from .filters import RecipeFilter
from users.serializers import SubRecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination
    permission_classes = (RecipePermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
            )

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.cre_obj(request.user, Favourites, pk)
        elif request.method == 'DELETE':
            return self.del_obj(request.user, Favourites, pk)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        basket = Basket.objects.filter(author=request.user)
        content_dict = {}
        for content in basket:
            ingredients = AmountOfIngredients.objects.filter(
                recipe=content.recipe
                )
            for ingredient in ingredients:
                name = ingredient.ingredients.name
                amount = ingredient.amount
                measurement_unit = ingredient.ingredients.measurement_unit
                if name not in content_dict:
                    content_dict[name] = {
                        'amount': amount,
                        'measurement_unit': measurement_unit
                    }
                else:
                    content_dict[name]['amount'] = (
                        content_dict[name]['amount'] + amount
                    )
        content_list = []
        for content in content_dict:
            content_list.append(
                f'{content}: {content_dict[content]["amount"]} '
                f'{content_dict[content]["measurement_unit"]}\n'
                )
        return HttpResponse(content_list, headers={
            'Content-Type': 'text/plain',
            'Content-Disposition': 'attachment; filename="shopping_cart"'
        })

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.cre_obj(request.user, Basket, pk)
        elif request.method == 'DELETE':
            return self.del_obj(request.user, Basket, pk)

    def cre_obj(self, user, model, pk):
        if model.objects.filter(author=user, recipe__id=pk).exists():
            return Response(
                {'errors': 'рецепт уже в списке'}, status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(author=user, recipe=recipe)
        serializer = SubRecipeSerializer(recipe)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def del_obj(self, user, model, pk):
        if not model.objects.filter(author=user, recipe__id=pk):
            return Response({'errors': 'рецепт в списке отсутствует'})
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.filter(author=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
