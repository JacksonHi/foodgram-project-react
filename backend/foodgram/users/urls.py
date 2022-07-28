from django.urls import path, include


app_name = 'urls'

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt'))
]
