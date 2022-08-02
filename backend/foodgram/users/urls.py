from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import CastomUserViewSet


app_name = 'users'

router = SimpleRouter()
router.register('users', CastomUserViewSet)

urlpatterns = [
    path('', include(router.register)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
