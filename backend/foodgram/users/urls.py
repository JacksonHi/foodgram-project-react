from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import FollowViewSet


app_name = 'urls'

router = SimpleRouter()
router.register('subscribe', FollowViewSet)

urlpatterns = [
    path('', include(router.register)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
