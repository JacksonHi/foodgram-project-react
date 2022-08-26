from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from api.models import User

from .pagination import SubscriptionPagination
from .models import Follow
from users.serializers import FollowSerializer


class CastomUserViewSet(UserViewSet):
    pagination_class = SubscriptionPagination

    @action(detail=False)
    def subscriptions(self, request):
        """Список подписок"""
        user = get_object_or_404(User, id=request.user.id)
        follow = user.follower.all()
        serializer = FollowSerializer(follow, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            elif Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Уже подписался'}, status.HTTP_400_BAD_REQUEST)
            follow = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                follow, context={'request': request}
            )
            return Response(serializer.data, status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if not Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Вы не подписаны'},
                    status.HTTP_400_BAD_REQUEST
                    )
            Follow.objects.filter(user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
