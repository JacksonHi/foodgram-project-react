from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import IngredientViewSet, TagViewSet


app_name = 'api'

router = SimpleRouter()
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]