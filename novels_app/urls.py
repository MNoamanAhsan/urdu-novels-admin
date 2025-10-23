from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryWithNovelsViewSet, search_novels

router = DefaultRouter()
router.register(r'home', CategoryWithNovelsViewSet, basename='home')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/search/', search_novels, name='search-novels'),
]