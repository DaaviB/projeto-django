from django.http import HttpRequest
from django.urls import reverse
from utils.pagination import make_pagination

from .test_recipe_base import RecipeTestBase


class MakePaginationTest(RecipeTestBase):
    def test_make_pagination_shows_correct_number_of_recipe_per_page(self):  # noqa: E501

        for ind in range(1, 21):
            self.make_recipe(
                slug=f'slug-the-number{ind}',
                author_data={
                    'username': f'User{ind}',

                }
            )
        url = reverse('recipes:home')
        response = self.client.get(url)
        self.assertEqual(9, response.context['recipes'].paginator.per_page)

    def test_make_pagination_raises_value_error_exception(self):
        request = HttpRequest()
        request.GET = {'page': ''}
        pagination = make_pagination(
            request,
            range(1, 21),
            1
        )

        self.assertEqual(1, pagination[1]['current_page'])
