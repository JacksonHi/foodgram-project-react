from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Ingredients, Tag, Recipe, Favourites, Basket
from .serializers import IngredientsSerializer, TagSerializer, RecipeSerializer
from users.serializers import SubRecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        #print(serializer)
        serializer.save(
            author=self.request.user
            )
    
    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.cre_obj(request.user, Favourites, pk)
        elif request.method == 'DELETE':
            return self.del_obj(request.user, Favourites, pk)
    
    def download_shopping_cart(self, request):
        pass

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.cre_obj(request.user, Basket, pk)
        elif request.method == 'DELETE':
            return self.del_obj(request.user, Basket, pk)

    def cre_obj(self, user, model, pk):
        if model.objects.filter(author=user, recipe__id=pk).exists():
            return Response({'errors': 'рецепт уже в списке'}, status.HTTP_400_BAD_REQUEST)
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
