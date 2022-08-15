from django.contrib.auth import get_user_model
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from users.models import Follow
from users.serializers import CastomUserSerializer
from .models import Ingredients, Recipe, Tag, AmountOfIngredients


User = get_user_model()


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['id', 'name', 'measurement_unit']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class AmountOfIngredientsSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = AmountOfIngredients
        fields = ['id', 'recipe', 'ingredients', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    author = CastomUserSerializer(read_only=True)
    ingredients = IngredientsSerializer(many=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
            'cooking_time', 'is_favorited', 'is_in_shopping_cart'
        ]
    
    def get_is_favorited(self, obj):
        user = self.context.get['request'].user
        return Follow.objects.filter(user=user, author=obj).exists

    def get_is_in_shopping_cart(self, obj):
        return True

    """def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            AmountOfIngredients.objects.create(recipe=recipe, **ingredient)
        return recipe"""
