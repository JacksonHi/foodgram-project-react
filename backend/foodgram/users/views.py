from djoser.views import UserViewSet
from rest_framework.decorators import action

from backend.foodgram.users.serializers import CastomUserSerializer


class CastomUserViewSet(UserViewSet):
    serializer_class = CastomUserSerializer

    @action(methods=['post'], detail=True)
    def subscribe():
        pass

    @action(methods=['delete'], detail=True, url_path='subscribe')    # изменить адрес на subscribe
    def unsubscribe():
        pass

    @action(methods=['get'], detail=False)
    def subscriptions():
        pass
