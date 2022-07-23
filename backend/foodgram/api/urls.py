from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import IngredientViewSet


router = SimpleRouter()
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]