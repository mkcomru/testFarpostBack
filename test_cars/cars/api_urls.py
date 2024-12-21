# cars/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CarViewSet

router = DefaultRouter()
router.register(r'cars', CarViewSet)

urlpatterns = [
    path('', include(router.urls)),
]