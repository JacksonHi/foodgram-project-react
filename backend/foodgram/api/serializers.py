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
    id = serializers.ReadOnlyField()
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')
    name = serializers.ReadOnlyField(source='ingredient.name')
    amount = serializers.ReadOnlyField(source='ingredient.amount')


    class Meta:
        model = AmountOfIngredients
        fields = ['id', 'name', 'measurement_unit', 'amount']  # id, name, amount, measurement_unit


class RecipeSerializer(serializers.ModelSerializer):
    """не работают ингредиенты"""
    author = CastomUserSerializer(read_only=True)
    ingredients = AmountOfIngredientsSerializer(many=True)
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
        user = self.context.get('request').user
        return Recipe.objects.filter(favourite__author=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return Recipe.objects.filter(basket__author=user, id=obj.id).exists()

    def validate(self, attrs):
        ingredients = self.initial_data.get('ingredients')
        #print(ingredients)
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
        #print('ingr')
        #print(recipe)
        #print(ingredients)
        for ingredient in ingredients:
            #print(ingredient)
            AmountOfIngredients.objects.create(
                recipe=recipe,
                ingredients_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
    
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags =self.initial_data.get('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.create_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        AmountOfIngredients.objects.filter(recipe__id=recipe.id)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.image = validated_data.get('image')
        instance.text = validated_data.get('text')
        instance.cooking_time =validated_data.get('cooking_time')
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        ingredients = validated_data.pop('ingredients')
        self.create_ingredients(ingredients, instance)
        instance.save()
        return instance


