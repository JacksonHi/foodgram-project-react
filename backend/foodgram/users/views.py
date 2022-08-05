from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from api.models import User
from .models import Follow

from users.serializers import FollowSerializer


class CastomUserViewSet(UserViewSet):
    @action(detail=False)    # Не видит 
    def subscriptions(self, request):
        """Список подписок"""
        print('hhhh')
        follow = Follow.objects.filter(following__user=request.user)
        serializer = FollowSerializer(follow, many=True)
        # serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id=None):
        """Добавить, удалить подписку"""
        queryset = User.objects.all()
        author = get_object_or_404(queryset, id=id)
        user = request.user
        if request.method == 'POST':
            follow = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(follow, request)
            serializer.is_valid()
            return Response(serializer.data, status.HTTP_201_CREATED)
        Follow.objects.filter(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

