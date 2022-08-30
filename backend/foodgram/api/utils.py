from django.http import HttpResponse

from recipes.models import AmountOfIngredients


def download_cart(request):
    content_dict = {}
    ingredients = AmountOfIngredients.objects.filter(
        recipe__basket__author=request.user,
    )
    for ingredient in ingredients:
        name = ingredient.ingredients.name
        amount = ingredient.amount
        measurement_unit = ingredient.ingredients.measurement_unit
        if name not in content_dict:
            content_dict[name] = {
                'amount': amount,
                'measurement_unit': measurement_unit
            }
        else:
            content_dict[name]['amount'] = (
                content_dict[name]['amount'] + amount
            )
    content_list = []
    for content in content_dict:
        content_list.append(
            f'{content}: {content_dict[content]["amount"]} '
            f'{content_dict[content]["measurement_unit"]}\n'
            )
    return HttpResponse(content_list, headers={
        'Content-Type': 'text/plain',
        'Content-Disposition': 'attachment; filename="shopping_cart"'
    })
