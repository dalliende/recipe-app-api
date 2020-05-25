from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from core.models import Tag
from core.models import Ingredient

from recipe.serializers import RecipeSerializer
from recipe.serializers import RecipeDetailSerializer


RECIPE_URL = reverse('recipe:recipe-list')


def detail_recipe_url(recipe_id):
    """Return recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id, ])


def sample_recipe(user, **params):
    """ Create and return a sample recipe"""
    defaults = {
        'title': 'Sample Recipe',
        'time_minutes': 10,
        'price': 5.00,
    }
    defaults.update(params)
    return Recipe.objects.create(
        user=user,
        **defaults,
    )


def sample_tag(user, name='main course'):
    """ create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='salt'):
    """ create and return a sample Ingredient"""
    return Ingredient.objects.create(user=user, name=name)


class PublicRecipeApiTest(TestCase):
    """Test publicly recipe API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that the authentication is required"""

        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPItest(TestCase):
    """ Test authenticated recipe API Access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@recipe.com',
            password='test1234'
        )
        self.client.force_authenticate(self.user)

    def test_retriving_recipes(self):
        """Test retirving a list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retriving_limited_to_user_recipes(self):
        """Test retirving a list of recipes"""
        user2 = get_user_model().objects.create(
            email='testing2@recipe.com',
            password='testing2'
        )
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)
        sample_recipe(user=user2, title='hola')

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user).order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """ Test viewing recipe detail view"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_recipe_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)
