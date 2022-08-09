from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Follow

User = get_user_model()


class CastomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed']

    def get_is_subscribed(self, obj):
        try:
            user = self.context.get('request').user
        except:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class CastomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password']


class FollowSerializer(serializers.Serializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    #recipes = serializers.SerializerMethodField()
    #recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        field = ['email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed']

    def get_is_subscribed(self, obj):
        return True

    #def get_recipes(self, obj):

    #def get_recipes_count(self, obj):

    """def create(self, validated_data):
        return Follow.objects.create(**validated_data)"""
