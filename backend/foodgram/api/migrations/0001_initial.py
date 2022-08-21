# Generated by Django 4.0.5 on 2022-08-18 20:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AmountOfIngredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(verbose_name='количество')),
            ],
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='название')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='единицы измерения')),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'ингредиенты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='название')),
                ('color', models.CharField(choices=[('#00FF00', 'Green'), ('#FF0000', 'Red'), ('#0000FF', 'Blue')], max_length=100)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='название')),
                ('image', models.ImageField(upload_to='', verbose_name='картинка')),
                ('text', models.TextField(verbose_name='описание')),
                ('cooking_time', models.PositiveSmallIntegerField(verbose_name='время на приготовление')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ingredients', models.ManyToManyField(related_name='recipes', through='api.AmountOfIngredients', to='api.ingredients', verbose_name='ингредиенты')),
                ('tags', models.ManyToManyField(related_name='recipes', to='api.tag', verbose_name='таг')),
            ],
        ),
        migrations.AddConstraint(
            model_name='ingredients',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_ingredients'),
        ),
        migrations.AddField(
            model_name='favourites',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='favourites',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite', to='api.recipe', verbose_name='рецепт'),
        ),
        migrations.AddField(
            model_name='basket',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket', to=settings.AUTH_USER_MODEL, verbose_name='корзина'),
        ),
        migrations.AddField(
            model_name='basket',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket', to='api.recipe', verbose_name='корзина'),
        ),
        migrations.AddField(
            model_name='amountofingredients',
            name='ingredients',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingrediernts', to='api.ingredients', verbose_name='ингредиент'),
        ),
        migrations.AddField(
            model_name='amountofingredients',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to='api.recipe', verbose_name='рецепт'),
        ),
    ]
