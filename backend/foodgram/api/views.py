from rest_framework import viewsets
from .models import Ingredients
from .serializers import IngredientsSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer