from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsAPITest(TestCase):
    """ Test the publicly available ingredientes API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test thjat login is required to access the endpoint"""

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITest(TestCase):
    """ Test private Ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            password='test123',
            email='test@recipe.com'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """ Test retrieving a list of ingredients"""
        Ingredient.objects.create(
            user=self.user,
            name='salt'
        )
        Ingredient.objects.create(
            user=self.user,
            name='sugar'
        )

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_ingredients_limited_to_user(self):
        """Test that only the ingredients for the
        authenticated user are returned"""
        user2 = get_user_model().objects.create(
            email='test2@recipe.com',
            password='test123',
        )
        Ingredient.objects.create(
            user=user2,
            name='peper'
        )
        Ingredient.objects.create(
            user=self.user,
            name='salt'
        )
        Ingredient.objects.create(
            user=self.user,
            name='sugar'
        )
        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.filter(
            user=self.user).order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
