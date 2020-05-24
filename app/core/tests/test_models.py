from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Tag
from core.models import Ingredient


def sample_user(email='recipe@test.com', password='testpass'):
    """ Create a Sample User"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_succesful(self):
        """Test creating a new user with an email"""
        email = 'prueba@recipe.com'
        password = 'test1234'

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalized_email_user_create(self):
        """Test that the email is normalized when creating an user"""
        email = 'prueba@RECIPE.com'
        user = get_user_model().objects.create_user(
            email,
            'passwordtest',
        )

        self.assertEqual(email.lower(), user.email)

    def test_new_user_invalid_email(self):
        """Test creating user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                None,
                'Test123'
            )

    def test_create_superuser(self):
        """Test that a super user is created"""
        user = get_user_model().objects.create_superuser(
            email='prueba@recipe.com',
            password='test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test Ingredient string represenatation"""
        ingredient = Ingredient.objects.create(
            name='Cucumber',
            user=sample_user(),
        )

        self.assertEqual(str(ingredient), ingredient.name)
