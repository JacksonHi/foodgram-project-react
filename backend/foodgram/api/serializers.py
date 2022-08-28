from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers, exceptions
from drf_extra_fields.fields import Base64ImageField

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
    id = serializers.ReadOnlyField(source='ingredients.id')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')
    name = serializers.ReadOnlyField(source='ingredients.name')

    class Meta:
        model = AmountOfIngredients
        fields = ['id', 'name', 'measurement_unit', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    author = CastomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
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

    def get_ingredients(self, obj):
        queryset = AmountOfIngredients.objects.filter(recipe=obj)
        serializer = AmountOfIngredientsSerializer(queryset, many=True)
        return serializer.data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            favourite__author=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return None
        return Recipe.objects.filter(basket__author=user, id=obj.id).exists()

    def validate(self, attrs):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Нужен хотя-бы один ингридиент для рецепта'})
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(Ingredients,
                                           id=ingredient_item['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError('ингридиент уже существует')
            ingredient_list.append(ingredient)
            if int(ingredient_item['amount']) <= 0:
                raise serializers.ValidationError({
                    'ingredients': ('количество не может быть <= 0')
                })
        attrs['ingredients'] = ingredients
        tags = self.initial_data.get('tags')
        if not tags:
            raise exceptions.ValidationError(
                'Нужно добавить хотя бы один таг.'
            )
        return attrs

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            AmountOfIngredients.objects.create(
                recipe=recipe,
                ingredients_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = self.initial_data.get('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        AmountOfIngredients.objects.filter(recipe__id=recipe.id)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        if validated_data.get('image') is not None:
            instance.image = validated_data.get('image')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        instance.ingredients.clear()
        AmountOfIngredients.objects.filter(recipe=instance).delete()
        ingredients = validated_data.get('ingredients')
        self.create_ingredients(ingredients, instance)
        instance.save()
        return instance
