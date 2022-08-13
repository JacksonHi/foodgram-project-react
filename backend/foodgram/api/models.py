from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredients(models.Model):
    name = models.CharField(
        verbose_name='название',
        max_length=200
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
                fields=['name', 'measurement_unit'],
                name='unique_ingredients'
                )
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """завтрак, обуед,ужин"""
    COLOR_CHOICES = [
        ('#00FF00', 'Green'),
        ('#FF0000', 'Red'),
        ('#0000FF', 'Blue'),
    ]
    name = models.CharField(
        verbose_name='название',
        max_length=256
    )
    color = models.CharField(choices=COLOR_CHOICES, max_length=100)
    slug = models.SlugField()

    class meta:
        ordering = ['name']
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'color', 'slug'],
                name='unique_tag'
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name='название',
        max_length=256
    )
    image = models.ImageField(verbose_name='картинка')
    text = models.TextField(verbose_name='описание')
    ingredients = models.ManyToManyField(
        Ingredients,
        related_name='recipes',
        verbose_name='ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='таг'
    )
    cooking_time = models.PositiveSmallIntegerField(verbose_name='время на приготовление')

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
        related_name='recipe',
        verbose_name='рецепт'
    )
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='ingrediernts',
        verbose_name='ингредиент'
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
        related_name='favourite',
        verbose_name='пользователь'
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourite',
        verbose_name='рецепт',
    )

    class meta:
        verbose_name='избранное'
        constraints = [
            models.UniqueConstraint(fields=['recipe',],
                                    name='unique favorites recipe')
        ]


class Basket(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='basket',
        verbose_name='корзина'
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='basket',
        verbose_name='корзина'
    )

    class meta:
        verbose_name='корзина'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique basket author')
        ]
