from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .utils import download_cart
from .filters import IngredientFilter, RecipeFilter
from recipes.models import (Basket, Favourites, Ingredients,
                            Recipe, Tag)
from users.models import Follow
from .pagination import MyPagination
from .permissions import RecipePermission
from .serializers import (IngredientsSerializer, RecipeSerializer,
                          TagSerializer, FollowSerializer,
                          SubRecipeSerializer)

User = get_user_model()


class CastomUserViewSet(UserViewSet):
    @action(detail=False, pagination_class=MyPagination)
    def subscriptions(self, request):
        """Список подписок"""
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id=None):
        """Добавить, удалить подписку"""
        queryset = User.objects.all()
        author = get_object_or_404(queryset, id=id)
        user = request.user
        if request.method == 'POST':
            if user == author:
                return Response(
                    {'errors': 'Нельзя подписаться на себя'},
                    status.HTTP_400_BAD_REQUEST
                    )
            if Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Уже подписался'}, status.HTTP_400_BAD_REQUEST)
            follow = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                follow, context={'request': request}
            )
            return Response(serializer.data, status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Вы не подписаны'},
                    status.HTTP_400_BAD_REQUEST
                    )
            Follow.objects.filter(user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = RecipeSerializer
    pagination_class = MyPagination
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
        if request.method == 'DELETE':
            return self.del_obj(request.user, Favourites, pk)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        return download_cart(request)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.cre_obj(request.user, Basket, pk)
        if request.method == 'DELETE':
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
