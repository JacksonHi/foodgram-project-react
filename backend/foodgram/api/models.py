from django.db import models
from django.contrib.auth import get_user_model
from colorfield.fields import ColorField
# from users.models import User


User = get_user_model()


class Ingredients(models.Model):
    name = models.CharField(
        verbose_name='название',
        max_length=200,
        unique=True
    )
    measurement_unit = models.CharField(
        verbose_name='единицы измерения',
        max_length=200
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement'],
                name='unique_ingredients'
                )
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """переделать на список 'завтрак','обуед','ужин'"""
    title = models.CharField(
        verbose_name='название',
        max_length=256
    )
    color = ColorField(default='#FF0000')
    slug = models.SlugField()

    class meta:
        ordering = ['title']
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'slug'],
                name='unique_tag'
            )
        ]

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(
        verbose_name='название',
        max_length=256
    )
    image = models.ImageField(verbose_name='картинка')
    description = models.TextField(verbose_name='описание')
    ingredients = models.ManyToManyField(
        Ingredients,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes',
        verbose_name='ингредиенты'
    )
    tag = models.ManyToManyField(
        Tag,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes',
        verbose_name='таг'
    )
    cooking_time = models.TimeField(verbose_name='время на приготовление')

    class meta:
        ordering = ['-id']
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.title


class AmountOfIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='рецепт',
        verbose_name='ingredients'
    )
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='ингредиент',
        verbose_name='ingrediernts'
    )
    amount = models.PositiveSmallIntegerField(verbose_name='количество')

    class meta:
        ordering = ['-id']
        verbose_name = 'коливчество ингридиента'
        verbose_name_plural = 'количество ингридиентов'


class Favourites(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='пользователь',
        verbose_name='favourite'
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='рецепт',
        verbose_name='favourite',
        unique=True
    )

    class meta:
        verbose_name='избранное'


class Basket(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='пользователь',
        verbose_name='favourite'
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='рецепт',
        verbose_name='favourite',
        unique=True
    )

    class meta:
        verbose_name='корзина'
