from django.contrib.auth import get_user_model
from rest_framework import serializers, exceptions
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
    id = serializers.ReadOnlyField(source='ingredien.id')
    recipe = serializers.ReadOnlyField(source='ingredient.id')
    ingredients = serializers.ReadOnlyField(source='ingredients.name')
    amount = serializers.ReadOnlyField(source='ingredient.amount')


    class Meta:
        model = AmountOfIngredients
        fields = ['id', 'recipe', 'ingredients', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    author = CastomUserSerializer(read_only=True)
    ingredients = AmountOfIngredientsSerializer(
        read_only=True,
        many=True
        )
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'tags', 'author', 'ingredients', 'name', 'image', 'text',
            'cooking_time', 'is_favorited', 'is_in_shopping_cart'
        ]
    
    def get_is_favorited(self, obj):
        """user = self.context.get['request'].user
        print(user)
        return Follow.objects.filter(user=user, author=obj).exists"""
        return True

    def get_is_in_shopping_cart(self, obj):
        return True

    def validate(self, attrs):
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError("finish must occur after start")
        return data
        """
        return super().validate(attrs)

    def validate_tags(self, value):
        if not value:
            raise exceptions.ValidationError(
                'Нужно добавить хотя бы один тег.'
            )

        return value

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            AmountOfIngredients.objects.create(
                recipe=recipe,
                ingredients_id=ingredient['id'],
                amount=ingredient['amount']
            )

    def create(self, validated_data):
        ingredients = self.initial_data.get('ingredients')
        tags =self.initial_data.get('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        r = AmountOfIngredients.objects.filter(recipe__id=84)
        recipe.ingredients.set(r)
        return recipe

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)