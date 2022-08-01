from djoser.views import UserViewSet

from backend.foodgram.users.serializers import CastomUserSerializer


class CastomUserViewSet(UserViewSet):
    serializer_class = CastomUserSerializer

    def subscribe():
        pass

    def unsubscribe():
        pass

    def subscriptions():
        pass
