from django.db import models
from django.contrib.auth import get_user_model
from colorfield.fields import ColorField
# from users.models import User


User = get_user_model()

class MeasurementUnit(models.Model):
    title = models.CharField(
        verbose_name='название',
        max_length=256
    )

    def __str__(self):
        return self.title


class Ingredients(models.Model):
    name = models.CharField(
        verbose_name='название',
        max_length=256,
        unique=True
    )
    quantity = models.FloatField(verbose_name='количество')
    measurement_unit = models.ForeignKey(
        MeasurementUnit,
        on_delete=models.PROTECT,
        related_name='measurement_unit',
        verbose_name='единицы измерения'
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    title = models.CharField(
        verbose_name='название',
        max_length=256
    )
    color = ColorField(default='#FF0000')
    slug = models.SlugField(unique=True)

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
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ingredients',
        verbose_name='ингредиенты'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tag',
        verbose_name='таг'
    )
    cooking_time = models.TimeField(verbose_name='время на приготовление')

    def __str__(self):
        return self.title
