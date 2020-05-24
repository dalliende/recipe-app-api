from django.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from recipe.views import TagViewSet
from recipe.views import IngredientViewSet

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path(
        '',
        include(router.urls),
    )
]
