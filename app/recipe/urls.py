from django.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from recipe.views import TagViewSet
from recipe.views import IngredientViewSet
from recipe.views import RecipeViewSet

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path(
        '',
        include(router.urls),
    )
]
