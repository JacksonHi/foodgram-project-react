from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from .views import CastomUserViewSet


app_name = 'users'

router = DefaultRouter()
router.register('users', CastomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
