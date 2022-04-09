from django.test import TestCase
from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):

    def setUp(self):
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='Davi',
            last_name='Brito',
            username='User',
            password='1234',
            email='user@user.com',
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Pessoas',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
            cover=','
        )
        return super().setUp()
