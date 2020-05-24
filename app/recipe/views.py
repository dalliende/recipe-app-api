from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from core.models import Ingredient

from recipe.serializers import TagSerializer
from recipe.serializers import IngredientSerializer


class BaseRecipeViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """Base viewset to manage the models"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Return objects for the current user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ Add user when creating the object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeViewSet):
    """ Manage Tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseRecipeViewSet):
    """ Manage Ingredient in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
