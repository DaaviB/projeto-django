from unittest.mock import patch

from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):

    def make_recipe_category_pagination(self, qty=9):
        category = self.make_category('CategoryTest')
        for i in range(qty):
            Recipe.objects.create(
                category=category,
                author=self.make_author(username=f"user{i}"),
                title='RecipeTest{i}',
                description='Descriçãooo',
                slug=f'slug-number-of-{i}',
                preparation_time=6,
                preparation_time_unit='Minutos',
                servings=2,
                servings_unit='Pessoas',
                preparation_steps='Assim depois assado',
                preparation_steps_is_html=False,
                is_published=True,
            )
        return category
        ...

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 100})
        )
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_return_404_if_no_recipes_not_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 100})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        # need a recipe for test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:category', kwargs={
                    'category_id': recipe.category.id})
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_is_paginated(self):
        category = self.make_recipe_category_pagination(qty=8)
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(
                reverse(
                    'recipes:category', kwargs={'category_id': category.id}
                ))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)
