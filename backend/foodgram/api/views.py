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
            return self.cre_obj(request, Favourites, pk)
        elif request.method == 'DELETE':
            return self.del_obj(request, pk)
    
    def download_shopping_cart(self, request):
        pass

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            self.cre_obj(request, Basket, pk)
        elif request.method == 'DELETE':
            self.del_obj(request, Basket, pk)

    def cre_obj(self, request, model, pk):
        """AttributeError: Got AttributeError when attempting to get a value for field `name` on serializer `SubRecipeSerializer`.
The serializer field might be named incorrectly and not match any attribute or key on the `Favourites` instance.
Original exception text was: 'Favourites' object has no attribute 'name'."""
        if model.objects.filter(author=request.user, recipe__id=pk).exists():
            return Response({'errors': 'кецепт уже есть в избранном'}, status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        cre = model.objects.create(author=request.user, recipe=recipe)
        serializer = SubRecipeSerializer(cre)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def del_obj(self, request, model, pk):
        pass
